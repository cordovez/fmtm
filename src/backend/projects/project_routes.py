# Copyright (c) 2022, 2023 Humanitarian OpenStreetMap Team
#
# This file is part of FMTM.
#
#     FMTM is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     FMTM is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with FMTM.  If not, see <https:#www.gnu.org/licenses/>.
#

from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from pathlib import Path
import json
import epdb

from ..db import database
from ..central import central_crud
from . import project_crud, project_schemas

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    dependencies=[Depends(database.get_db)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[project_schemas.ProjectOut])
async def read_projects(
        user_id: int = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db),
):
    projects = project_crud.get_projects(db, user_id, skip, limit)
    return projects


@router.post("/near_me", response_model=project_schemas.ProjectSummary)
def get_task(lat: float, long: float, user_id: int = None):
    return "Coming..."


@router.get("/summaries", response_model=List[project_schemas.ProjectSummary])
async def read_project_summaries(
    user_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
):
    projects = project_crud.get_project_summaries(db, user_id, skip, limit)
    return projects


@router.get("/{project_id}", response_model=project_schemas.ProjectOut)
async def read_project(project_id: int, db: Session = Depends(database.get_db)):
    project = project_crud.get_project_by_id(db, project_id)
    if project:
        return project
    else:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post("/delete/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(database.get_db)):
    """Delete a project from ODK Central and the local database"""
    # FIXME: should check for errors
    odkproject = central_crud.delete_odk_project(project_id)
    project = project_crud.delete_project_by_id(db, project_id)
    if project:
        return project
    else:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post("/beta/create_project", response_model=project_schemas.ProjectOut)
async def create_project(
    project_info: project_schemas.BETAProjectUpload,
    db: Session = Depends(database.get_db),
):
    """Create a project in ODK Central and the local database"""
    odkproject = central_crud.create_odk_project(project_info.project_info.name)
    # Use the ID we get from Central, as it's needed for many queries
    project_info.project_info.id = odkproject['id']
    # TODO check token against user or use token instead of passing user
    project = project_crud.create_project_with_project_info(db, project_info)
    return project


@router.post("/beta/{project_id}/upload", response_model=project_schemas.ProjectOut)
async def upload_project_boundary(
    project_id: int,
    project_name_prefix: str,
    task_type_prefix: str,
    upload: UploadFile,
    db: Session = Depends(database.get_db),
):
    """This uploads the projecy boundzry polygon to an existing project"""
    # TODO: consider replacing with this: https://stackoverflow.com/questions/73442335/how-to-upload-a-large-file-%e2%89%a53gb-to-fastapi-backend/73443824#73443824
    project = project_crud.update_project_with_zip(
        db, project_id, project_name_prefix, task_type_prefix, upload
    )
    return f"{project}"

@router.post("/{project_id}/upload")
async def upload_project_boundary(
    project_id: int,
    upload: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    # read entire file
    content = await upload.read()
    #epdb.st()
    boundary = json.loads(content)

    result = project_crud.update_project_boundary(db, project_id, boundary)
    if not result:
        raise HTTPException(
            status_code=428, detail=f"Project with id {project_id} does not exist"
        )
        return f"No project with id {project_id}"

    return {f"Message": f"{project_id}"}

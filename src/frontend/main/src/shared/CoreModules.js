
import {
    Card,
    CardContent,
    Typography,
    Stack,
    Box,
    Button,
    InputBase,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Slide,
    IconButton,
    Tabs,
    Tab,
    Divider,
    List,
    ListItem,
    ListItemText,
    Menu,
    Alert as MuiAlert,
    Snackbar,
    AppBar,
    Toolbar,
    Grid,
    Pagination,
    ThemeProvider,
    CssBaseline,
    Paper,
    createTheme,
    Container
} from "@mui/material";
import axios from 'axios'
import { Navigation as SwiperNavigation, Pagination as SwiperPagination } from "swiper";
import { Swiper, SwiperSlide } from 'swiper/react';
import Skeleton, { SkeletonTheme } from 'react-loading-skeleton'
import { useNavigate, useParams, Link, Outlet, RouterProvider, createBrowserRouter } from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux';
import { createSlice, configureStore } from "@reduxjs/toolkit";
import { combineReducers } from 'redux'
export default {
    RouterProvider,
    createBrowserRouter,
    Card,
    CardContent,
    useNavigate,
    useParams,
    useSelector,
    useDispatch,
    Stack,
    Box,
    Typography,
    Button,
    InputBase,
    Skeleton,
    SkeletonTheme,
    createSlice,
    configureStore,
    combineReducers,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Slide,
    IconButton,
    Tabs,
    Tab,
    Divider,
    List,
    ListItem,
    ListItemText,
    Menu,
    MuiAlert,
    Snackbar,
    AppBar,
    Toolbar,
    Link,
    Grid,
    Pagination,
    ThemeProvider,
    CssBaseline,
    Paper,
    createTheme,
    Outlet,
    Container,
    SwiperNavigation,
    SwiperPagination,
    Swiper,
    SwiperSlide,
    axios
}
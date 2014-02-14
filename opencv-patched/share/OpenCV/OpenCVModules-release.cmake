#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
SET(CMAKE_IMPORT_FILE_VERSION 1)

# Compute the installation prefix relative to this file.
GET_FILENAME_COMPONENT(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_FILE}" PATH)
GET_FILENAME_COMPONENT(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
GET_FILENAME_COMPONENT(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)

# Import target "opencv_core" for configuration "Release"
SET_PROPERTY(TARGET opencv_core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_core PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_core.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_core.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_core )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_core "${_IMPORT_PREFIX}/lib/libopencv_core.so.3.0.0" )

# Import target "opencv_flann" for configuration "Release"
SET_PROPERTY(TARGET opencv_flann APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_flann PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_flann.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_flann.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_flann )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_flann "${_IMPORT_PREFIX}/lib/libopencv_flann.so.3.0.0" )

# Import target "opencv_imgproc" for configuration "Release"
SET_PROPERTY(TARGET opencv_imgproc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_imgproc PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_imgproc.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_imgproc.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_imgproc )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_imgproc "${_IMPORT_PREFIX}/lib/libopencv_imgproc.so.3.0.0" )

# Import target "opencv_highgui" for configuration "Release"
SET_PROPERTY(TARGET opencv_highgui APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_highgui PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "opencv_core;opencv_imgproc"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_highgui.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_highgui.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_highgui )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_highgui "${_IMPORT_PREFIX}/lib/libopencv_highgui.so.3.0.0" )

# Import target "opencv_features2d" for configuration "Release"
SET_PROPERTY(TARGET opencv_features2d APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_features2d PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_features2d.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_features2d.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_features2d )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_features2d "${_IMPORT_PREFIX}/lib/libopencv_features2d.so.3.0.0" )

# Import target "opencv_calib3d" for configuration "Release"
SET_PROPERTY(TARGET opencv_calib3d APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_calib3d PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_calib3d.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_calib3d.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_calib3d )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_calib3d "${_IMPORT_PREFIX}/lib/libopencv_calib3d.so.3.0.0" )

# Import target "opencv_cudaarithm" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudaarithm APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudaarithm PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudaarithm.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudaarithm.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudaarithm )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudaarithm "${_IMPORT_PREFIX}/lib/libopencv_cudaarithm.so.3.0.0" )

# Import target "opencv_ml" for configuration "Release"
SET_PROPERTY(TARGET opencv_ml APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_ml PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_ml.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_ml.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_ml )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_ml "${_IMPORT_PREFIX}/lib/libopencv_ml.so.3.0.0" )

# Import target "opencv_nonfree" for configuration "Release"
SET_PROPERTY(TARGET opencv_nonfree APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_nonfree PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_cudaarithm"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_nonfree.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_nonfree.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_nonfree )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_nonfree "${_IMPORT_PREFIX}/lib/libopencv_nonfree.so.3.0.0" )

# Import target "opencv_objdetect" for configuration "Release"
SET_PROPERTY(TARGET opencv_objdetect APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_objdetect PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_imgproc;opencv_highgui;opencv_ml"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_objdetect.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_objdetect.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_objdetect )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_objdetect "${_IMPORT_PREFIX}/lib/libopencv_objdetect.so.3.0.0" )

# Import target "opencv_video" for configuration "Release"
SET_PROPERTY(TARGET opencv_video APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_video PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_imgproc"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_video.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_video.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_video )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_video "${_IMPORT_PREFIX}/lib/libopencv_video.so.3.0.0" )

# Import target "opencv_contrib" for configuration "Release"
SET_PROPERTY(TARGET opencv_contrib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_contrib PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_cudaarithm;opencv_ml;opencv_nonfree;opencv_objdetect;opencv_video"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_contrib.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_contrib.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_contrib )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_contrib "${_IMPORT_PREFIX}/lib/libopencv_contrib.so.3.0.0" )

# Import target "opencv_cudawarping" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudawarping APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudawarping PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_imgproc"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudawarping.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudawarping.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudawarping )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudawarping "${_IMPORT_PREFIX}/lib/libopencv_cudawarping.so.3.0.0" )

# Import target "opencv_cuda" for configuration "Release"
SET_PROPERTY(TARGET opencv_cuda APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cuda PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_cudaarithm;opencv_cudawarping;opencv_ml;opencv_objdetect"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cuda.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cuda.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cuda )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cuda "${_IMPORT_PREFIX}/lib/libopencv_cuda.so.3.0.0" )

# Import target "opencv_cudafilters" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudafilters APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudafilters PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_cudaarithm;opencv_imgproc"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudafilters.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudafilters.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudafilters )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudafilters "${_IMPORT_PREFIX}/lib/libopencv_cudafilters.so.3.0.0" )

# Import target "opencv_cudaimgproc" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudaimgproc APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudaimgproc PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_cudaarithm;opencv_imgproc;opencv_cudafilters"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudaimgproc.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudaimgproc.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudaimgproc )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudaimgproc "${_IMPORT_PREFIX}/lib/libopencv_cudaimgproc.so.3.0.0" )

# Import target "opencv_legacy" for configuration "Release"
SET_PROPERTY(TARGET opencv_legacy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_legacy PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_ml;opencv_video"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_legacy.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_legacy.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_legacy )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_legacy "${_IMPORT_PREFIX}/lib/libopencv_legacy.so.3.0.0" )

# Import target "opencv_cudabgsegm" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudabgsegm APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudabgsegm PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_cudaarithm;opencv_cudafilters;opencv_cudaimgproc;opencv_ml;opencv_video;opencv_legacy"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudabgsegm.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudabgsegm.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudabgsegm )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudabgsegm "${_IMPORT_PREFIX}/lib/libopencv_cudabgsegm.so.3.0.0" )

# Import target "opencv_cudacodec" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudacodec APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudacodec PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_imgproc;opencv_highgui"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudacodec.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudacodec.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudacodec )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudacodec "${_IMPORT_PREFIX}/lib/libopencv_cudacodec.so.3.0.0" )

# Import target "opencv_cudafeatures2d" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudafeatures2d APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudafeatures2d PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_cudaarithm;opencv_imgproc;opencv_cudafilters;opencv_cudawarping;opencv_flann;opencv_highgui;opencv_features2d"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudafeatures2d.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudafeatures2d.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudafeatures2d )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudafeatures2d "${_IMPORT_PREFIX}/lib/libopencv_cudafeatures2d.so.3.0.0" )

# Import target "opencv_cudaoptflow" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudaoptflow APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudaoptflow PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_cudaarithm;opencv_cudafilters;opencv_cudaimgproc;opencv_cudawarping;opencv_ml;opencv_video;opencv_legacy"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudaoptflow.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudaoptflow.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudaoptflow )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudaoptflow "${_IMPORT_PREFIX}/lib/libopencv_cudaoptflow.so.3.0.0" )

# Import target "opencv_cudastereo" for configuration "Release"
SET_PROPERTY(TARGET opencv_cudastereo APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_cudastereo PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_cudastereo.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_cudastereo.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_cudastereo )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_cudastereo "${_IMPORT_PREFIX}/lib/libopencv_cudastereo.so.3.0.0" )

# Import target "opencv_optim" for configuration "Release"
SET_PROPERTY(TARGET opencv_optim APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_optim PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_optim.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_optim.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_optim )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_optim "${_IMPORT_PREFIX}/lib/libopencv_optim.so.3.0.0" )

# Import target "opencv_photo" for configuration "Release"
SET_PROPERTY(TARGET opencv_photo APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_photo PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_cudaarithm;opencv_imgproc;opencv_cudafilters;opencv_cudaimgproc"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_photo.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_photo.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_photo )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_photo "${_IMPORT_PREFIX}/lib/libopencv_photo.so.3.0.0" )

# Import target "opencv_softcascade" for configuration "Release"
SET_PROPERTY(TARGET opencv_softcascade APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_softcascade PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_imgproc;opencv_ml"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_softcascade.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_softcascade.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_softcascade )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_softcascade "${_IMPORT_PREFIX}/lib/libopencv_softcascade.so.3.0.0" )

# Import target "opencv_shape" for configuration "Release"
SET_PROPERTY(TARGET opencv_shape APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_shape PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_imgproc;opencv_video"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_shape.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_shape.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_shape )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_shape "${_IMPORT_PREFIX}/lib/libopencv_shape.so.3.0.0" )

# Import target "opencv_stitching" for configuration "Release"
SET_PROPERTY(TARGET opencv_stitching APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_stitching PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_cudaarithm;opencv_cudawarping;opencv_ml;opencv_objdetect;opencv_cuda;opencv_cudafilters;opencv_cudafeatures2d;opencv_nonfree"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_stitching.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_stitching.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_stitching )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_stitching "${_IMPORT_PREFIX}/lib/libopencv_stitching.so.3.0.0" )

# Import target "opencv_superres" for configuration "Release"
SET_PROPERTY(TARGET opencv_superres APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_superres PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_cudaarithm;opencv_cudacodec;opencv_cudafilters;opencv_cudaimgproc;opencv_cudawarping;opencv_ml;opencv_video;opencv_legacy;opencv_cudaoptflow"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_superres.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_superres.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_superres )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_superres "${_IMPORT_PREFIX}/lib/libopencv_superres.so.3.0.0" )

# Import target "opencv_ts" for configuration "Release"
SET_PROPERTY(TARGET opencv_ts APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_ts PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_imgproc;opencv_highgui;dl;m;pthread;rt"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_ts.a"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_ts )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_ts "${_IMPORT_PREFIX}/lib/libopencv_ts.a" )

# Import target "opencv_videostab" for configuration "Release"
SET_PROPERTY(TARGET opencv_videostab APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(opencv_videostab PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "opencv_core;opencv_flann;opencv_imgproc;opencv_highgui;opencv_features2d;opencv_calib3d;opencv_cudaarithm;opencv_cudawarping;opencv_ml;opencv_objdetect;opencv_cuda;opencv_cudafilters;opencv_cudaimgproc;opencv_video;opencv_legacy;opencv_cudaoptflow;opencv_photo"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopencv_videostab.so.3.0.0"
  IMPORTED_SONAME_RELEASE "libopencv_videostab.so.3.0"
  )

LIST(APPEND _IMPORT_CHECK_TARGETS opencv_videostab )
LIST(APPEND _IMPORT_CHECK_FILES_FOR_opencv_videostab "${_IMPORT_PREFIX}/lib/libopencv_videostab.so.3.0.0" )

# Loop over all imported files and verify that they actually exist
FOREACH(target ${_IMPORT_CHECK_TARGETS} )
  FOREACH(file ${_IMPORT_CHECK_FILES_FOR_${target}} )
    IF(NOT EXISTS "${file}" )
      MESSAGE(FATAL_ERROR "The imported target \"${target}\" references the file
   \"${file}\"
but this file does not exist.  Possible reasons include:
* The file was deleted, renamed, or moved to another location.
* An install or uninstall procedure did not complete successfully.
* The installation package was faulty and contained
   \"${CMAKE_CURRENT_LIST_FILE}\"
but not all the files it references.
")
    ENDIF()
  ENDFOREACH()
  UNSET(_IMPORT_CHECK_FILES_FOR_${target})
ENDFOREACH()
UNSET(_IMPORT_CHECK_TARGETS)

# Cleanup temporary variables.
SET(_IMPORT_PREFIX)

# Commands beyond this point should not need to know the version.
SET(CMAKE_IMPORT_FILE_VERSION)

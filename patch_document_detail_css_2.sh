#!/bin/bash
sed -i '' '/<\/head>/i\
<!-- Drawer Style Mobile UI Fixes -->\
<style>\
@media (max-width: 768px) {\
    .pdf-controls {\
        display: none !important;\
    }\
    .pdf-viewer {\
        height: 100% !important;\
    }\
    .pdf-viewer > div > div:first-child {\
        padding: 4px !important;\
        margin-bottom: 4px !important;\
        gap: 4px !important;\
        top: 0 !important;\
        border-radius: 0 !important;\
        width: 100% !important;\
        justify-content: center !important;\
        flex-wrap: wrap !important;\
    }\
    .pdf-viewer > div > div:first-child button {\
        padding: 4px !important;\
    }\
    .pdf-viewer > div > div:first-child i {\
        font-size: 14px !important;\
    }\
    #image-scroll-container {\
        max-height: calc(100% - 40px) !important;\
        min-height: auto !important;\
        height: 100% !important;\
    }\
}\
</style>\
' document-detail.html

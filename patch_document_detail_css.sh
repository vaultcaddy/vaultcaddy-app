#!/bin/bash
sed -i '' '/<\/head>/i\
<!-- Drawer Style Mobile UI -->\
<style>\
@media (max-width: 768px) {\
    body {\
        overflow: hidden !important; /* Prevent body scroll */\
    }\
    .dashboard-container {\
        height: 100vh !important;\
        display: flex !important;\
        flex-direction: column !important;\
    }\
    .main-content {\
        flex: 1 !important;\
        display: flex !important;\
        flex-direction: column !important;\
        height: 100% !important;\
        overflow: hidden !important;\
    }\
    .detail-container {\
        flex: 1 !important;\
        display: flex !important;\
        flex-direction: column !important;\
        height: calc(100vh - 80px) !important;\
        gap: 0 !important;\
        padding: 0 !important;\
        position: relative !important;\
    }\
    .pdf-preview-panel {\
        order: 1 !important;\
        height: 40% !important;\
        max-height: 40% !important;\
        flex-shrink: 0 !important;\
        border-bottom: none !important;\
        border-radius: 0 !important;\
        box-shadow: none !important;\
        background: #000 !important;\
        z-index: 1 !important;\
    }\
    .pdf-viewer {\
        height: calc(100% - 30px) !important;\
        max-height: none !important;\
        background: #000 !important;\
    }\
    .pdf-controls {\
        height: 30px !important;\
        background: rgba(0,0,0,0.8) !important;\
        border-radius: 0 !important;\
        width: 100% !important;\
    }\
    .data-panel {\
        order: 2 !important;\
        flex: 1 !important;\
        height: 60% !important;\
        overflow-y: auto !important;\
        background: #f3f4f6 !important;\
        padding: 12px 8px !important;\
        border-radius: 16px 16px 0 0 !important;\
        box-shadow: 0 -4px 12px rgba(0,0,0,0.1) !important;\
        z-index: 2 !important;\
        margin-top: -10px !important;\
    }\
    /* Add a drag handle indicator */\
    .data-panel::before {\
        content: "";\
        display: block;\
        width: 40px;\
        height: 4px;\
        background: #d1d5db;\
        border-radius: 2px;\
        margin: 0 auto 12px auto;\
    }\
}\
</style>\
' document-detail.html

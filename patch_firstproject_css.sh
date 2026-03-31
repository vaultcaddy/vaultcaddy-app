#!/bin/bash
sed -i '' '/<\/head>/i\
<!-- Mobile UI Upgrades -->\
<style>\
@media (max-width: 768px) {\
    /* Table to Card Layout */\
    .table-container {\
        background: transparent !important;\
        box-shadow: none !important;\
        border: none !important;\
        padding: 0 !important;\
    }\
    .table-container table, .table-container table tbody {\
        display: block !important;\
        width: 100% !important;\
    }\
    .table-container table thead {\
        display: none !important;\
    }\
    .table-container table tr {\
        display: grid !important;\
        grid-template-columns: 32px 1fr auto !important;\
        grid-template-rows: auto auto auto !important;\
        gap: 4px 8px !important;\
        background: #fff !important;\
        margin-bottom: 12px !important;\
        border-radius: 12px !important;\
        padding: 12px !important;\
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;\
        border: 1px solid #f3f4f6 !important;\
        align-items: center !important;\
    }\
    .table-container table td {\
        display: block !important;\
        padding: 0 !important;\
        border: none !important;\
        text-align: left !important;\
        max-width: none !important;\
    }\
    .table-container table td:nth-child(1) {\
        grid-column: 1; grid-row: 1 / span 3;\
        display: flex !important; justify-content: center; align-items: center;\
    }\
    .table-container table td:nth-child(2) {\
        grid-column: 2; grid-row: 1;\
    }\
    .table-container table td:nth-child(2) span {\
        max-width: 140px !important;\
        font-size: 13px !important;\
        color: #6b7280 !important;\
    }\
    .table-container table td:nth-child(3) {\
        grid-column: 2; grid-row: 2;\
    }\
    .table-container table td:nth-child(3) div {\
        font-size: 15px !important; font-weight: 700 !important; color: #111827 !important;\
        max-width: 160px !important;\
    }\
    .table-container table td:nth-child(4) {\
        grid-column: 2; grid-row: 3;\
    }\
    .table-container table td:nth-child(4) span {\
        font-size: 11px !important; padding: 2px 6px !important;\
    }\
    .table-container table td:nth-child(5) {\
        grid-column: 3; grid-row: 1;\
        text-align: right !important;\
    }\
    .table-container table td:nth-child(5) span {\
        font-size: 10px !important; padding: 2px 6px !important;\
    }\
    .table-container table td:nth-child(6) {\
        grid-column: 3; grid-row: 2;\
        text-align: right !important;\
        font-size: 16px !important; font-weight: 800 !important; color: #047857 !important;\
    }\
    .table-container table td:nth-child(7) {\
        grid-column: 3; grid-row: 3;\
        text-align: right !important;\
        font-size: 11px !important; color: #9ca3af !important;\
    }\
    .table-container table td:nth-child(8), .table-container table td:nth-child(9) {\
        display: none !important;\
    }\
    \
    /* Floating Action Button */\
    .mobile-fab {\
        display: flex !important;\
        position: fixed;\
        bottom: 24px;\
        right: 24px;\
        width: 56px;\
        height: 56px;\
        border-radius: 28px;\
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\
        color: white;\
        align-items: center;\
        justify-content: center;\
        font-size: 24px;\
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);\
        z-index: 999;\
        cursor: pointer;\
    }\
    /* Hide desktop upload button on mobile */\
    #action-buttons-container-mobile .btn-primary {\
        display: none !important;\
    }\
}\
@media (min-width: 769px) {\
    .mobile-fab {\
        display: none !important;\
    }\
}\
</style>\
' firstproject.html

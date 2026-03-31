#!/bin/bash
sed -i '' '/<\/head>/i\
<!-- Mobile UI Upgrades -->\
<style>\
@media (max-width: 768px) {\
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
}\
@media (min-width: 769px) {\
    .mobile-fab {\
        display: none !important;\
    }\
}\
</style>\
' dashboard.html

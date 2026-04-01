
// 🔥 在瀏覽器控制台運行此腳本來強制刷新

console.log('=== 🔍 VaultCaddy 診斷工具 ===');
console.log('');

// 1. 檢查 Firebase 用戶
firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
        console.log('✅ Firebase 用戶已登入');
        console.log('   Email:', user.email);
        console.log('   DisplayName:', user.displayName);
        console.log('   第一個字母:', user.displayName ? user.displayName.charAt(0) : user.email.charAt(0));
    } else {
        console.log('❌ Firebase 用戶未登入');
    }
});

// 2. 檢查 getUserInitial 函數
console.log('');
console.log('=== getUserInitial 函數測試 ===');
if (typeof getUserInitial === 'function') {
    console.log('✅ getUserInitial 存在');
    console.log('   返回值:', getUserInitial());
} else {
    console.log('❌ getUserInitial 不存在');
}

// 3. 檢查會員頭像
console.log('');
console.log('=== 會員頭像檢查 ===');
const avatar = document.getElementById('userAvatar');
if (avatar) {
    console.log('✅ userAvatar 元素存在');
    console.log('   當前文字:', avatar.textContent);
    console.log('   Display:', window.getComputedStyle(avatar).display);
} else {
    console.log('❌ userAvatar 元素不存在');
}

// 4. 強制更新頭像（測試）
console.log('');
console.log('=== 強制更新測試 ===');
if (avatar && window.userDisplayName) {
    const newInitial = userDisplayName.charAt(0).toUpperCase();
    avatar.textContent = newInitial;
    console.log('✅ 已強制更新為:', newInitial);
    console.log('   如果現在顯示正確，說明是緩存問題');
    console.log('   請使用無痕模式或清除站點數據後重新測試');
}

// 5. 檢查 Export 菜單（僅 firstproject.html）
if (document.getElementById('exportMenu')) {
    console.log('');
    console.log('=== Export 菜單檢查 ===');
    const menu = document.getElementById('exportMenu');
    const style = window.getComputedStyle(menu);
    console.log('✅ Export 菜單存在');
    console.log('   Display:', style.display);
    console.log('   Position:', style.position);
    console.log('   Z-index:', style.zIndex);
    console.log('   Top:', style.top);
    console.log('   Left:', style.left);
}

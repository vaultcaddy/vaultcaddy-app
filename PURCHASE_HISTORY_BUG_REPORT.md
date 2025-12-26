
╔════════════════════════════════════════════════════════════════════╗
║         🐛 Purchase History 数据不一致问题 - 根本原因分析      ║
╚════════════════════════════════════════════════════════════════════╝

【🎯 根本原因】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  问题代码位置：account.html (所有4个语言版本)
  
  ```javascript
  async function loadCreditsHistory() {
      const tbody = document.getElementById('credits-history-tbody');
      const filter = document.getElementById('history-month-filter').value;
      
      // ❌ 问题：在这里等待 loadMonthOptions()
      await loadMonthOptions();  // ← 这行代码会查询 Firebase
      
      try {
          // ... 后续代码 ...
      }
  }
  
  async function loadMonthOptions() {
      try {
          // ❌ 问题：再次查询 Firebase 获取所有记录
          const historySnapshot = await firebase.firestore()
              .collection('users')
              .doc(userId)
              .collection('creditsHistory')
              .orderBy('createdAt', 'desc')
              .get();  // ← 可能超时或失败
          
          // ... 生成月份选项 ...
      } catch (error) {
          console.error('載入月份選項失敗:', error);
          // ❌ 问题：错误被静默吞掉，没有通知用户
      }
  }
  ```


【🔍 为什么会导致不一致】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  场景1：英文版和中文版卡住
  ─────────────────────────────────────────────────────────────
  1. 用户打开页面
  2. loadCreditsHistory() 开始执行
  3. await loadMonthOptions() 开始查询 Firebase
  4. ❌ loadMonthOptions() 查询超时或失败
  5. ❌ 因为使用了 await，loadCreditsHistory() 一直等待
  6. ❌ 页面卡在 "Loading records..." 状态
  7. ❌ catch 块捕获错误但没有更新 UI
  
  
  场景2：日文版和韩文版成功
  ─────────────────────────────────────────────────────────────
  1. 用户打开页面
  2. loadCreditsHistory() 开始执行
  3. await loadMonthOptions() 开始查询 Firebase
  4. ✅ loadMonthOptions() 查询成功
  5. ✅ loadCreditsHistory() 继续执行
  6. ✅ 查询成功并显示记录
  
  
  场景3：记录数量不同（9 vs 7）
  ─────────────────────────────────────────────────────────────
  1. 日文版：打开时有9条记录
  2. 用户删除了2条记录（或自然过期）
  3. 韩文版：稍后打开时只有7条记录
  4. ✅ 这是正常的，因为数据确实变化了


【🔧 修复方案】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  修复1：移除重复的 Firebase 查询
  ─────────────────────────────────────────────────────────────
  ```javascript
  async function loadCreditsHistory() {
      const tbody = document.getElementById('credits-history-tbody');
      const filter = document.getElementById('history-month-filter').value;
      
      try {
          // 检查是否有登入用户
          if (!window.simpleAuth || !window.simpleAuth.currentUser) {
              tbody.innerHTML = `...请先登录...`;
              return;
          }
          
          const userId = window.simpleAuth.currentUser.uid;
          
          // ✅ 修复：一次性获取所有数据
          let query = firebase.firestore()
              .collection('users')
              .doc(userId)
              .collection('creditsHistory')
              .orderBy('createdAt', 'desc');
          
          const historySnapshot = await query.limit(50).get();
          
          // ✅ 修复：使用获取到的数据生成月份选项
          generateMonthOptionsFromData(historySnapshot);
          
          // ✅ 修复：使用相同的数据显示记录
          displayCreditsHistory(historySnapshot, filter);
          
      } catch (error) {
          console.error('❌ 加载失败:', error);
          tbody.innerHTML = `
              <tr>
                  <td colspan="3" style="text-align: center; padding: 2rem; color: #ef4444;">
                      ⚠️ 加载失败: ${error.message}
                      <br>
                      <button onclick="loadCreditsHistory()" 
                              style="margin-top: 1rem; padding: 0.5rem 1rem; 
                                     background: #3b82f6; color: white; 
                                     border: none; border-radius: 6px; 
                                     cursor: pointer;">
                          重试
                      </button>
                  </td>
              </tr>
          `;
      }
  }
  
  // ✅ 新函数：从已有数据生成月份选项（不再查询 Firebase）
  function generateMonthOptionsFromData(historySnapshot) {
      const select = document.getElementById('history-month-filter');
      
      if (historySnapshot.empty) {
          return;
      }
      
      const months = new Set();
      historySnapshot.forEach(doc => {
          const record = doc.data();
          if (record.createdAt) {
              const date = record.createdAt.toDate();
              const yearMonth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
              months.add(yearMonth);
          }
      });
      
      const sortedMonths = Array.from(months).sort((a, b) => b.localeCompare(a));
      const currentValue = select.value;
      
      // 保留第一个选项（"所有记录"/"All Records"等）
      const firstOption = select.options[0];
      select.innerHTML = '';
      select.appendChild(firstOption);
      
      sortedMonths.forEach(yearMonth => {
          const [year, month] = yearMonth.split('-');
          const option = document.createElement('option');
          option.value = yearMonth;
          option.textContent = `${parseInt(month)}/${year}`;
          select.appendChild(option);
      });
      
      if (sortedMonths.includes(currentValue)) {
          select.value = currentValue;
      }
  }
  ```
  
  
  修复2：添加超时保护
  ─────────────────────────────────────────────────────────────
  ```javascript
  async function loadCreditsHistory() {
      const tbody = document.getElementById('credits-history-tbody');
      
      // ✅ 添加超时保护
      const timeoutId = setTimeout(() => {
          tbody.innerHTML = `
              <tr>
                  <td colspan="3" style="text-align: center; padding: 2rem; color: #f59e0b;">
                      ⏱️ 加载超时，请检查网络连接
                      <br>
                      <button onclick="loadCreditsHistory()" 
                              style="margin-top: 1rem; padding: 0.5rem 1rem;">
                          重试
                      </button>
                  </td>
              </tr>
          `;
      }, 10000); // 10秒超时
      
      try {
          // ... 查询代码 ...
          
          clearTimeout(timeoutId); // ✅ 清除超时
      } catch (error) {
          clearTimeout(timeoutId); // ✅ 清除超时
          // ... 错误处理 ...
      }
  }
  ```
  
  
  修复3：添加详细的调试日志
  ─────────────────────────────────────────────────────────────
  ```javascript
  async function loadCreditsHistory() {
      console.log('🔄 [1/5] 开始加载购买历史...');
      console.log('🔍 当前用户:', window.simpleAuth?.currentUser?.uid);
      
      try {
          if (!window.simpleAuth || !window.simpleAuth.currentUser) {
              console.error('❌ [2/5] 用户未登录');
              return;
          }
          
          const userId = window.simpleAuth.currentUser.uid;
          console.log('✅ [2/5] 用户ID:', userId);
          
          console.log('🔍 [3/5] 开始查询 Firebase...');
          const historySnapshot = await query.limit(50).get();
          console.log('✅ [3/5] 查询完成，记录数量:', historySnapshot.size);
          
          console.log('🔍 [4/5] 生成月份选项...');
          generateMonthOptionsFromData(historySnapshot);
          console.log('✅ [4/5] 月份选项已生成');
          
          console.log('🔍 [5/5] 渲染记录...');
          displayCreditsHistory(historySnapshot, filter);
          console.log('✅ [5/5] 加载完成！');
          
      } catch (error) {
          console.error('❌ 加载失败:', error);
          console.error('错误详情:', error.message, error.code, error.stack);
      }
  }
  ```


【📊 修复后的预期效果】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────────────────────────────────────────────────┐
  │ ✅ 所有4个语言版本都能成功加载                             │
  │ ✅ 减少 Firebase 查询次数（从2次减少到1次）               │
  │ ✅ 如果加载失败，显示明确的错误信息和重试按钮             │
  │ ✅ 10秒超时保护，不会永远卡住                              │
  │ ✅ 详细的Console日志，方便排查问题                         │
  │ ✅ 所有版本显示相同的数据（来自同一个 Firebase 集合）     │
  └─────────────────────────────────────────────────────────────┘


【🚀 实施步骤】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. 修改 account.html（中文版）
  2. 修改 en/account.html（英文版）
  3. 修改 jp/account.html（日文版）
  4. 修改 kr/account.html（韩文版）
  5. 测试所有4个版本
  6. 上传到服务器


【📝 技术总结】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  根本问题：
  • 重复的 Firebase 查询（loadMonthOptions + loadCreditsHistory）
  • 缺少超时保护
  • 错误处理不完善（静默失败）
  • 缺少详细的调试日志
  
  修复策略：
  • 单次查询，数据复用
  • 添加超时保护
  • 用户友好的错误提示
  • 详细的调试日志


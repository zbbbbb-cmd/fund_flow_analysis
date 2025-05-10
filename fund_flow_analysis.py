# import akshare as ak
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime, timedelta
# import tkinter as tk
# from tkinter import ttk, messagebox, scrolledtext
# import matplotlib
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# import numpy as np
# import threading
# import re

# # 设置中文字体
# matplotlib.use("TkAgg")
# plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
# plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# class StockAnalysisApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("A股资金流向与指数关系分析")
#         self.root.geometry("1200x800")
#         self.root.minsize(1000, 700)
        
#         # 数据缓存
#         self.current_data = None
        
#         # 创建界面
#         self.create_widgets()
        
#         # 检查akshare版本
#         self.check_akshare_version()
        
#     def check_akshare_version(self):
#         """检查akshare版本并显示提示"""
#         try:
#             version = ak.__version__
#             self.status_var.set(f"已加载 akshare v{version}")
#             # 检查是否为较新版本
#             major, minor, _ = map(int, re.findall(r'\d+', version)[:3])
#             if major < 1 or (major == 1 and minor < 30):
#                 messagebox.showinfo("版本提示", 
#                     f"您的akshare版本为{version}，建议升级到最新版本以获取最佳兼容性。\n"
#                     "可通过命令: 'pip install akshare --upgrade' 进行升级。")
#         except Exception as e:
#             print(f"检查akshare版本时出错: {e}")
#             self.status_var.set("无法确定akshare版本，请确保已安装最新版本")
    
#     def create_widgets(self):
#         # 创建主框架
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # 控制面板
#         control_frame = ttk.LabelFrame(main_frame, text="分析参数设置", padding="10")
#         control_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # 指数选择
#         ttk.Label(control_frame, text="选择指数:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
#         self.index_var = tk.StringVar(value="sh000001")
#         index_frame = ttk.Frame(control_frame)
#         index_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
#         index_options = [
#             ("上证指数", "sh000001"),
#             ("深证成指", "sz399001"),
#             ("创业板指", "sz399006")
#         ]
        
#         for i, (text, value) in enumerate(index_options):
#             ttk.Radiobutton(index_frame, text=text, variable=self.index_var, value=value).grid(row=0, column=i, padx=10)
        
#         # 时间周期选择
#         ttk.Label(control_frame, text="时间周期:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
#         self.period_var = tk.StringVar(value="30d")
#         period_frame = ttk.Frame(control_frame)
#         period_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
#         period_options = [
#             ("近30天", "30d"),
#             ("近90天", "90d"),
#             ("近6个月", "180d"),
#             ("近1年", "365d")
#         ]
        
#         for i, (text, value) in enumerate(period_options):
#             ttk.Radiobutton(period_frame, text=text, variable=self.period_var, value=value).grid(row=0, column=i, padx=10)
        
#         # 分析按钮
#         self.analyze_btn = ttk.Button(control_frame, text="开始分析", command=self.start_analysis)
#         self.analyze_btn.grid(row=0, column=2, rowspan=2, padx=20, pady=5, sticky=tk.EW)
        
#         # 状态栏
#         self.status_var = tk.StringVar(value="就绪")
#         self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
#         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
#         # 结果区域 - 使用Notebook创建选项卡
#         self.notebook = ttk.Notebook(main_frame)
#         self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
#         # 概览选项卡
#         self.overview_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.overview_frame, text="分析概览")
        
#         # 趋势图选项卡
#         self.trend_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.trend_frame, text="资金与指数趋势")
        
#         # 散点图选项卡
#         self.scatter_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.scatter_frame, text="相关性分析")
        
#         # 数据表格选项卡
#         self.data_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.data_frame, text="详细数据")
        
#         # 创建趋势图
#         self.trend_fig = Figure(figsize=(10, 5), dpi=100)
#         self.trend_ax = self.trend_fig.add_subplot(111)
#         self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, master=self.trend_frame)
#         self.trend_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
#         # 创建散点图
#         self.scatter_fig = Figure(figsize=(10, 5), dpi=100)
#         self.scatter_ax = self.scatter_fig.add_subplot(111)
#         self.scatter_canvas = FigureCanvasTkAgg(self.scatter_fig, master=self.scatter_frame)
#         self.scatter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
#         # 创建数据表格
#         columns = ("日期", "指数收盘价", "涨跌幅(%)", "北向资金净流入(亿)", "主力资金净流入(亿)")
#         self.data_tree = ttk.Treeview(self.data_frame, columns=columns, show="headings")
        
#         for col in columns:
#             self.data_tree.heading(col, text=col)
#             self.data_tree.column(col, width=150, anchor=tk.CENTER)
        
#         scrollbar = ttk.Scrollbar(self.data_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
#         self.data_tree.configure(yscroll=scrollbar.set)
        
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.data_tree.pack(fill=tk.BOTH, expand=True)
        
#         # 导出按钮
#         self.export_btn = ttk.Button(self.data_frame, text="导出数据", command=self.export_data)
#         self.export_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
#         # 创建概览卡片
#         self.create_overview_cards()
        
#     def create_overview_cards(self):
#         # 清除现有卡片
#         for widget in self.overview_frame.winfo_children():
#             widget.destroy()
        
#         # 创建卡片框架
#         card_frame = ttk.Frame(self.overview_frame, padding="10")
#         card_frame.pack(fill=tk.BOTH, expand=True)
        
#         # 北向资金相关性卡片
#         self.north_card = ttk.LabelFrame(card_frame, text="北向资金相关性", padding="10")
#         self.north_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        
#         self.north_value = tk.StringVar(value="--")
#         ttk.Label(self.north_card, textvariable=self.north_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.north_card, text="北向资金净流入与指数涨跌幅的相关系数").pack()
        
#         # 主力资金相关性卡片
#         self.main_card = ttk.LabelFrame(card_frame, text="主力资金相关性", padding="10")
#         self.main_card.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)
        
#         self.main_value = tk.StringVar(value="--")
#         ttk.Label(self.main_card, textvariable=self.main_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.main_card, text="主力资金净流入与指数涨跌幅的相关系数").pack()
        
#         # 资金协同性卡片
#         self.fund_card = ttk.LabelFrame(card_frame, text="资金协同性", padding="10")
#         self.fund_card.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)
        
#         self.fund_value = tk.StringVar(value="--")
#         ttk.Label(self.fund_card, textvariable=self.fund_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.fund_card, text="北向资金与主力资金的协同系数").pack()
        
#         # 设置权重，使卡片均匀分布
#         card_frame.grid_columnconfigure(0, weight=1)
#         card_frame.grid_columnconfigure(1, weight=1)
#         card_frame.grid_columnconfigure(2, weight=1)
#         card_frame.grid_rowconfigure(0, weight=1)
        
#     def parse_time_period(self, period):
#         """解析时间周期参数"""
#         if period.endswith('d'):
#             days = int(period[:-1])
#             return timedelta(days=days)
#         elif period.endswith('m'):
#             months = int(period[:-1])
#             return timedelta(days=months*30)  # 粗略估算每月30天
#         else:
#             raise ValueError(f"无效的时间周期格式: {period}。请使用如'30d'(30天),'6m'(6个月)的格式。")
    
#     def start_analysis(self):
#         """开始分析"""
#         # 禁用按钮
#         self.analyze_btn.config(state=tk.DISABLED)
#         self.status_var.set("正在获取数据...")
        
#         # 在单独的线程中执行分析，避免阻塞UI
#         analysis_thread = threading.Thread(target=self.perform_analysis)
#         analysis_thread.daemon = True
#         analysis_thread.start()
    
#     def perform_analysis(self):
#         try:
#             # 获取参数
#             index_code = self.index_var.get()
#             period = self.period_var.get()
            
#             # 解析时间周期
#             time_delta = self.parse_time_period(period)
            
#             # 设置时间范围
#             end_date = datetime.now()
#             start_date = end_date - time_delta
            
#             # 获取指数名称
#             index_names = {
#                 "sh000001": "上证指数",
#                 "sz399001": "深证成指",
#                 "sz399006": "创业板指"
#             }
#             index_name = index_names.get(index_code, "未知指数")
            
#             # 更新状态
#             self.update_status(f"正在获取{index_name}数据...")
            
#             # 获取数据
#             index_data = self.get_market_index_data(index_code, start_date, end_date)
#             if index_data is None or index_data.empty:
#                 raise Exception(f"无法获取{index_name}数据")
            
#             self.update_status("正在获取北向资金数据...")
#             north_data = self.get_north_flow_data(start_date, end_date)
#             if north_data is None or north_data.empty:
#                 raise Exception("无法获取北向资金数据")
            
#             self.update_status("正在获取主力资金数据...")
#             main_data = self.get_main_money_flow_data(start_date, end_date)
#             if main_data is None or main_data.empty:
#                 raise Exception("无法获取主力资金数据")
            
#             self.update_status("正在合并和分析数据...")
            
#             # 合并数据
#             merged_data = self.merge_data(index_data, north_data, main_data)
#             if merged_data is None or merged_data.empty:
#                 raise Exception("合并数据失败")
            
#             # 保存当前数据
#             self.current_data = merged_data
            
#             # 计算相关系数
#             correlations = self.calculate_correlations(merged_data)
            
#             # 更新UI
#             self.root.after(0, lambda: self.update_results(merged_data, index_name, correlations))
            
#             self.update_status("分析完成")
#         except Exception as e:
#             # 显示错误信息
#             self.root.after(0, lambda: messagebox.showerror("分析错误", str(e)))
#             self.update_status("分析失败")
#         finally:
#             # 重新启用按钮
#             self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
    
#     def update_status(self, message):
#         """更新状态栏"""
#         self.status_var.set(message)
#         self.root.update_idletasks()
    
#     def get_market_index_data(self, index_code, start_date, end_date):
#         """获取指定指数的历史数据"""
#         try:
#             if index_code == "sh000001":  # 上证指数
#                 df = ak.stock_zh_index_daily(symbol="sh000001")
#             elif index_code == "sz399001":  # 深证成指
#                 df = ak.stock_zh_index_daily(symbol="sz399001")
#             elif index_code == "sz399006":  # 创业板指
#                 df = ak.stock_zh_index_daily(symbol="sz399006")
#             else:
#                 print(f"暂不支持该指数: {index_code}")
#                 return None
                
#             # 转换日期格式并筛选数据
#             df['date'] = pd.to_datetime(df['date'])
#             df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
#             # 计算涨跌幅(%)
#             df['pct_change'] = df['close'].pct_change() * 100
            
#             return df
#         except Exception as e:
#             print(f"获取指数数据时出错: {e}")
#             return None
    
#     def get_north_flow_data(self, start_date, end_date):
#         """获取北向资金净流入数据（兼容多种akshare版本）"""
#         try:
#             # 尝试最新接口
#             try:
#                 df = ak.stock_hsgt_north_net_flow_in_em(symbol="北向资金")
#                 df['date'] = pd.to_datetime(df['date'])
#                 df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                 df = df.rename(columns={'net_amount': 'north_net_inflow'})
#                 # 转换为亿元单位
#                 df['north_net_inflow'] = df['north_net_inflow'] / 100000000
#                 return df[['date', 'north_net_inflow']]
#             except Exception as e1:
#                 print(f"尝试最新北向资金接口失败: {e1}")
                
#                 # 尝试旧接口
#                 try:
#                     df = ak.stock_individual_fund_flow_rank(market_type="北向")
#                     df['date'] = pd.to_datetime(df['日期'])
#                     df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                     df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
#                     return df[['date', 'north_net_inflow']]
#                 except Exception as e2:
#                     print(f"尝试旧北向资金接口失败: {e2}")
                    
#                     # 尝试备选接口
#                     try:
#                         df = ak.stock_market_fund_flow(indicator="北向资金")
#                         df['date'] = pd.to_datetime(df['日期'])
#                         df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                         df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
#                         return df[['date', 'north_net_inflow']]
#                     except Exception as e3:
#                         print(f"尝试备选北向资金接口失败: {e3}")
#                         raise Exception("无法获取北向资金数据，请确保akshare版本是最新的")
#         except Exception as e:
#             print(f"获取北向资金数据时出错: {e}")
#             return None
    
#     def get_main_money_flow_data(self, start_date, end_date):
#         """获取A股主力资金净流入数据（兼容多种akshare版本）"""
#         try:
#             # 尝试最新接口
#             try:
#                 df = ak.stock_market_fund_flow(indicator="大盘资金流")
#                 df['date'] = pd.to_datetime(df['日期'])
#                 df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                 df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
#                 return df[['date', 'main_net_inflow']]
#             except Exception as e1:
#                 print(f"尝试最新主力资金接口失败: {e1}")
                
#                 # 尝试旧接口
#                 try:
#                     df = ak.stock_individual_fund_flow_rank(market_type="A股")
#                     df['date'] = pd.to_datetime(df['日期'])
#                     df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                     df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
#                     return df[['date', 'main_net_inflow']]
#                 except Exception as e2:
#                     print(f"尝试旧主力资金接口失败: {e2}")
                    
#                     # 尝试备选接口
#                     try:
#                         df = ak.stock_market_fund_flow(indicator="今日")
#                         df['date'] = pd.to_datetime(df['日期'])
#                         df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                         df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
#                         return df[['date', 'main_net_inflow']]
#                     except Exception as e3:
#                         print(f"尝试备选主力资金接口失败: {e3}")
#                         raise Exception("无法获取主力资金数据，请确保akshare版本是最新的")
#         except Exception as e:
#             print(f"获取主力资金数据时出错: {e}")
#             return None
    
#     def merge_data(self, index_data, north_data, main_data):
#         """合并各类数据"""
#         try:
#             # 合并北向资金和主力资金数据
#             merged_data = pd.merge(north_data, main_data, on='date', how='outer')
            
#             # 合并指数数据
#             final_data = pd.merge(merged_data, index_data[['date', 'close', 'pct_change']], 
#                                 on='date', how='outer')
            
#             # 按日期排序
#             final_data = final_data.sort_values('date')
            
#             # 填充缺失值
#             final_data = final_data.fillna(method='ffill')
            
#             return final_data
#         except Exception as e:
#             print(f"合并数据时出错: {e}")
#             return None
    
#     def calculate_correlations(self, data):
#         """计算相关系数"""
#         if data is None or data.empty:
#             return None
        
#         correlations = {}
        
#         # 北向资金与指数涨跌幅的相关系数
#         if 'north_net_inflow' in data.columns and 'pct_change' in data.columns:
#             correlations['north'] = data['north_net_inflow'].corr(data['pct_change'])
        
#         # 主力资金与指数涨跌幅的相关系数
#         if 'main_net_inflow' in data.columns and 'pct_change' in data.columns:
#             correlations['main'] = data['main_net_inflow'].corr(data['pct_change'])
        
#         # 北向资金与主力资金的相关系数
#         if 'north_net_inflow' in data.columns and 'main_net_inflow' in data.columns:
#             correlations['fund'] = data['north_net_inflow'].corr(data['main_net_inflow'])
        
#         return correlations
    
#     def update_results(self, data, index_name, correlations):
#         """更新结果显示"""
#         # 更新概览卡片
#         if correlations and 'north' in correlations:
#             self.north_value.set(f"{correlations['north']:.2f}")
        
#         if correlations and 'main' in correlations:
#             self.main_value.set(f"{correlations['main']:.2f}")
        
#         if correlations and 'fund' in correlations:
#             self.fund_value.set(f"{correlations['fund']:.2f}")
        
#         # 绘制趋势图
#         self.trend_ax.clear()
        
#         if 'date' in data.columns and 'close' in data.columns:
#             dates = data['date'].dt.strftime('%Y-%m-%d')
#             line1 = self.trend_ax.plot(dates, data['close'], 'b-', label='指数收盘价')
#             self.trend_ax.set_ylabel('指数收盘价', color='b')
#             self.trend_ax.tick_params(axis='y', labelcolor='b')
            
#             ax2 = self.trend_ax.twinx()
            
#             if 'north_net_inflow' in data.columns:
#                 bars1 = ax2.bar(dates, data['north_net_inflow'], width=0.5, alpha=0.5, color='r', label='北向资金净流入')
            
#             if 'main_net_inflow' in data.columns:
#                 bars2 = ax2.bar(dates, data['main_net_inflow'], width=0.5, alpha=0.5, color='g', label='主力资金净流入')
            
#             ax2.set_ylabel('资金净流入(亿)', color='k')
#             ax2.tick_params(axis='y', labelcolor='k')
            
#             # 添加图例
#             lines, labels = self.trend_ax.get_legend_handles_labels()
#             lines2, labels2 = ax2.get_legend_handles_labels()
#             ax2.legend(lines + lines2, labels + labels2, loc='upper left')
            
#             # 设置标题和x轴标签
#             self.trend_ax.set_title(f'{index_name}与资金流向趋势图')
            
#             # 设置x轴刻度，避免过于密集
#             n = min(20, len(dates))  # 最多显示20个刻度
#             step = max(1, len(dates) // n)
#             self.trend_ax.set_xticks(range(0, len(dates), step))
#             self.trend_ax.set_xticklabels(dates[::step], rotation=45)
            
#             # 优化布局
#             self.trend_fig.tight_layout()
            
#             # 刷新画布
#             self.trend_canvas.draw()
        
#         # 绘制散点图
#         self.scatter_ax.clear()
        
#         if 'north_net_inflow' in data.columns and 'pct_change' in data.columns:
#             self.scatter_ax.scatter(data['north_net_inflow'], data['pct_change'], c='r', alpha=0.5, label='北向资金')
            
#         if 'main_net_inflow' in data.columns and 'pct_change' in data.columns:
#             self.scatter_ax.scatter(data['main_net_inflow'], data['pct_change'], c='g', alpha=0.5, label='主力资金')
        
#         self.scatter_ax.set_xlabel('资金净流入(亿)')
#         self.scatter_ax.set_ylabel('涨跌幅(%)')
#         self.scatter_ax.set_title(f'资金净流入与{index_name}涨跌幅关系')
#         self.scatter_ax.legend()
#         self.scatter_fig.tight_layout()
#         self.scatter_canvas.draw()
        
#         # 更新数据表格
#         # 清空现有数据
#         for item in self.data_tree.get_children():
#             self.data_tree.delete(item)
        
#         # 填充数据
#         if 'date' in data.columns:
#             for i, row in data.iterrows():
#                 date = row['date'].strftime('%Y-%m-%d')
#                 close = f"{row['close']:.2f}" if 'close' in row else "--"
#                 pct_change = f"{row['pct_change']:.2f}" if 'pct_change' in row else "--"
#                 north = f"{row['north_net_inflow']:.2f}" if 'north_net_inflow' in row else "--"
#                 main = f"{row['main_net_inflow']:.2f}" if 'main_net_inflow' in row else "--"
                
#                 self.data_tree.insert("", "end", values=(date, close, pct_change, north, main))
    
#     def export_data(self):
#         """导出数据到CSV文件"""
#         if self.current_data is None or self.current_data.empty:
#             messagebox.showinfo("导出数据", "没有数据可导出")
#             return
        
#         from tkinter import filedialog
        
#         # 获取保存路径
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".csv",
#             filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
#             title="保存数据"
#         )
        
#         if not file_path:
#             return
        
#         try:
#             # 保存数据
#             self.current_data.to_csv(file_path, index=False, encoding='utf-8-sig')
#             messagebox.showinfo("导出成功", f"数据已成功导出到 {file_path}")
#         except Exception as e:
#             messagebox.showerror("导出失败", f"导出数据时出错: {str(e)}")

# def main():
#     root = tk.Tk()
#     app = StockAnalysisApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()            

# 

# import akshare as ak
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime, timedelta
# import tkinter as tk
# from tkinter import ttk, messagebox, scrolledtext
# import matplotlib
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# import numpy as np
# import threading
# import re

# # 设置中文字体
# matplotlib.use("TkAgg")
# plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
# plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# class DatePicker(ttk.Frame):
#     """日期选择器组件"""
#     def __init__(self, parent, default_date=None):
#         super().__init__(parent)
#         self.parent = parent
        
#         # 如果没有提供默认日期，使用今天的日期
#         if default_date:
#             self.date_var = tk.StringVar(value=default_date.strftime('%Y-%m-%d'))
#         else:
#             self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        
#         # 创建日期输入框
#         self.date_entry = ttk.Entry(self, textvariable=self.date_var, width=12)
#         self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
#         # 创建日期选择按钮
#         self.date_btn = ttk.Button(self, text="??", command=self.select_date)
#         self.date_btn.pack(side=tk.LEFT)
    
#     def get_date(self):
#         """获取选择的日期"""
#         try:
#             return datetime.strptime(self.date_var.get(), '%Y-%m-%d')
#         except ValueError:
#             messagebox.showerror("日期格式错误", "请使用YYYY-MM-DD格式的日期")
#             return None
    
#     def select_date(self):
#         """打开日期选择对话框"""
#         # 这里使用简单的输入对话框，实际应用中可以使用更高级的日期选择器
#         from tkinter import simpledialog
        
#         current_date = self.date_var.get()
#         new_date = simpledialog.askstring("选择日期", "请输入日期 (YYYY-MM-DD):", 
#                                          initialvalue=current_date)
        
#         if new_date:
#             try:
#                 # 验证日期格式
#                 datetime.strptime(new_date, '%Y-%m-%d')
#                 self.date_var.set(new_date)
#             except ValueError:
#                 messagebox.showerror("日期格式错误", "请使用YYYY-MM-DD格式的日期")

# class StockAnalysisApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("A股资金流向与指数关系分析")
#         self.root.geometry("1200x800")
#         self.root.minsize(1000, 700)
        
#         # 数据缓存
#         self.current_data = None
        
#         # 北向资金开关
#         self.north_enabled = tk.BooleanVar(value=False)
        
#         # 创建界面
#         self.create_widgets()
        
#         # 检查akshare版本
#         self.check_akshare_version()
        
#     def check_akshare_version(self):
#         """检查akshare版本并显示提示"""
#         try:
#             version = ak.__version__
#             self.status_var.set(f"已加载 akshare v{version}")
#             # 检查是否为较新版本
#             major, minor, _ = map(int, re.findall(r'\d+', version)[:3])
#             if major < 1 or (major == 1 and minor < 30):
#                 messagebox.showinfo("版本提示", 
#                     f"您的akshare版本为{version}，建议升级到最新版本以获取最佳兼容性。\n"
#                     "可通过命令: 'pip install akshare --upgrade' 进行升级。")
#         except Exception as e:
#             print(f"检查akshare版本时出错: {e}")
#             self.status_var.set("无法确定akshare版本，请确保已安装最新版本")
    
#     def create_widgets(self):
#         # 创建主框架
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # 控制面板
#         control_frame = ttk.LabelFrame(main_frame, text="分析参数设置", padding="10")
#         control_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # 指数选择
#         ttk.Label(control_frame, text="选择指数:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
#         self.index_var = tk.StringVar(value="sh000001")
#         index_frame = ttk.Frame(control_frame)
#         index_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
#         index_options = [
#             ("上证指数", "sh000001"),
#             ("深证成指", "sz399001"),
#             ("创业板指", "sz399006"),
#             ("科创50", "sh000688"),  # 新增科创50指数
#             ("沪深300", "sh000300")   # 新增沪深300指数
#         ]
        
#         # 动态计算每行显示的指数选项数量
#         options_per_row = 3
#         for i, (text, value) in enumerate(index_options):
#             row = i // options_per_row
#             col = i % options_per_row
#             ttk.Radiobutton(index_frame, text=text, variable=self.index_var, value=value).grid(row=row, column=col, padx=10, pady=5)
        
#         # 日期选择
#         ttk.Label(control_frame, text="开始日期:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
#         self.start_date_picker = DatePicker(control_frame, datetime.now() - timedelta(days=30))
#         self.start_date_picker.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
#         ttk.Label(control_frame, text="结束日期:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
#         self.end_date_picker = DatePicker(control_frame, datetime.now())
#         self.end_date_picker.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
#         # 资金类型选择
#         ttk.Label(control_frame, text="关注资金:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
#         fund_frame = ttk.Frame(control_frame)
#         fund_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
#         self.north_check = ttk.Checkbutton(fund_frame, text="北向资金", variable=self.north_enabled)
#         self.north_check.grid(row=0, column=0, padx=5)
#         self.main_check = ttk.Checkbutton(fund_frame, text="主力资金", variable=tk.BooleanVar(value=True))
#         self.main_check.grid(row=0, column=1, padx=5)
        
#         # 分析按钮
#         self.analyze_btn = ttk.Button(control_frame, text="开始分析", command=self.start_analysis)
#         self.analyze_btn.grid(row=0, column=2, rowspan=5, padx=20, pady=5, sticky=tk.EW)
        
#         # 状态栏
#         self.status_var = tk.StringVar(value="就绪")
#         self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
#         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
#         # 结果区域 - 使用Notebook创建选项卡
#         self.notebook = ttk.Notebook(main_frame)
#         self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
#         # 概览选项卡
#         self.overview_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.overview_frame, text="分析概览")
        
#         # 趋势图选项卡
#         self.trend_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.trend_frame, text="资金与指数趋势")
        
#         # 散点图选项卡
#         self.scatter_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.scatter_frame, text="相关性分析")
        
#         # 数据表格选项卡
#         self.data_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.data_frame, text="详细数据")
        
#         # 创建趋势图
#         self.trend_fig = Figure(figsize=(10, 5), dpi=100)
#         self.trend_ax = self.trend_fig.add_subplot(111)
#         self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, master=self.trend_frame)
#         self.trend_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
#         # 创建散点图
#         self.scatter_fig = Figure(figsize=(10, 5), dpi=100)
#         self.scatter_ax = self.scatter_fig.add_subplot(111)
#         self.scatter_canvas = FigureCanvasTkAgg(self.scatter_fig, master=self.scatter_frame)
#         self.scatter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
#         # 创建数据表格
#         self.data_tree = ttk.Treeview(self.data_frame)
#         scrollbar = ttk.Scrollbar(self.data_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
#         self.data_tree.configure(yscroll=scrollbar.set)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.data_tree.pack(fill=tk.BOTH, expand=True)
        
#         # 导出按钮
#         self.export_btn = ttk.Button(self.data_frame, text="导出数据", command=self.export_data)
#         self.export_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
#         # 创建概览卡片
#         self.create_overview_cards()
    
#     def create_overview_cards(self):
#         # 初始卡片布局
#         self.north_card = ttk.LabelFrame(self.overview_frame, text="北向资金相关性", padding="10")
#         self.north_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
#         self.north_card.grid_remove()
        
#         self.main_card = ttk.LabelFrame(self.overview_frame, text="主力资金相关性", padding="10")
#         self.main_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        
#         self.fund_card = ttk.LabelFrame(self.overview_frame, text="资金协同性", padding="10")
#         self.fund_card.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)
#         self.fund_card.grid_remove()
        
#         self.north_value = tk.StringVar(value="--")
#         ttk.Label(self.north_card, textvariable=self.north_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.north_card, text="北向资金净流入与指数涨跌幅的相关系数").pack()
        
#         self.main_value = tk.StringVar(value="--")
#         ttk.Label(self.main_card, textvariable=self.main_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.main_card, text="主力资金净流入与指数涨跌幅的相关系数").pack()
        
#         self.fund_value = tk.StringVar(value="--")
#         ttk.Label(self.fund_card, textvariable=self.fund_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.fund_card, text="北向资金与主力资金的协同系数").pack()
        
#         # 设置列权重
#         self.overview_frame.grid_columnconfigure(0, weight=1)
#         self.overview_frame.grid_columnconfigure(1, weight=1)
#         self.overview_frame.grid_columnconfigure(2, weight=1)
    
#     def start_analysis(self):
#         """开始分析"""
#         # 禁用按钮
#         self.analyze_btn.config(state=tk.DISABLED)
#         self.status_var.set("正在获取数据...")
        
#         # 获取日期
#         start_date = self.start_date_picker.get_date()
#         end_date = self.end_date_picker.get_date()
        
#         # 验证日期
#         if not start_date or not end_date:
#             self.status_var.set("日期格式错误")
#             self.analyze_btn.config(state=tk.NORMAL)
#             return
        
#         if start_date >= end_date:
#             messagebox.showerror("日期错误", "开始日期必须早于结束日期")
#             self.status_var.set("就绪")
#             self.analyze_btn.config(state=tk.NORMAL)
#             return
        
#         # 在单独的线程中执行分析，避免阻塞UI
#         analysis_thread = threading.Thread(target=self.perform_analysis, args=(start_date, end_date))
#         analysis_thread.daemon = True
#         analysis_thread.start()
    
#     def perform_analysis(self, start_date, end_date):
#         try:
#             # 获取参数
#             index_code = self.index_var.get()
#             analyze_north = self.north_enabled.get()
#             analyze_main = True
            
#             # 获取指数名称
#             index_names = {
#                 "sh000001": "上证指数",
#                 "sz399001": "深证成指",
#                 "sz399006": "创业板指",
#                 "sh000688": "科创50",  # 新增科创50指数名称
#                 "sh000300": "沪深300"   # 新增沪深300指数名称
#             }
#             index_name = index_names.get(index_code, "未知指数")
            
#             # 更新状态
#             self.update_status(f"正在获取{index_name}数据...")
            
#             # 获取数据
#             index_data = self.get_market_index_data(index_code, start_date, end_date)
#             if index_data is None or index_data.empty:
#                 raise Exception(f"无法获取{index_name}数据")
            
#             north_data = None
#             if analyze_north:
#                 self.update_status("正在获取北向资金数据...")
#                 north_data = self.get_north_flow_data(start_date, end_date)
#                 if north_data is None or north_data.empty:
#                     raise Exception("无法获取北向资金数据")
            
#             self.update_status("正在获取主力资金数据...")
#             main_data = self.get_main_money_flow_data(start_date, end_date)
#             if main_data is None or main_data.empty:
#                 raise Exception("无法获取主力资金数据")
            
#             self.update_status("正在合并和分析数据...")
            
#             # 合并数据
#             merged_data = self.merge_data(index_data, north_data, main_data, analyze_north)
#             if merged_data is None or merged_data.empty:
#                 raise Exception("合并数据失败")
            
#             # 保存当前数据
#             self.current_data = merged_data
            
#             # 计算相关系数
#             correlations = self.calculate_correlations(merged_data, analyze_north)
            
#             # 更新UI
#             self.root.after(0, lambda: self.update_results(merged_data, index_name, correlations, analyze_north))
            
#             self.update_status("分析完成")
#         except Exception as e:
#             # 显示错误信息
#             self.root.after(0, lambda: messagebox.showerror("分析错误", str(e)))
#             self.update_status("分析失败")
#         finally:
#             # 重新启用按钮
#             self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
    
#     def update_status(self, message):
#         """更新状态栏"""
#         self.status_var.set(message)
#         self.root.update_idletasks()
    
#     def get_market_index_data(self, index_code, start_date, end_date):
#         """获取指定指数的历史数据"""
#         try:
#             # 特殊处理科创50和沪深300指数
#             if index_code == "sh000688":  # 科创50
#                 df = ak.stock_zh_index_daily(symbol="sh000688")
#             elif index_code == "sh000300":  # 沪深300
#                 df = ak.stock_zh_index_daily(symbol="sh000300")
#             elif index_code == "sh000001":
#                 df = ak.stock_zh_index_daily(symbol="sh000001")
#             elif index_code == "sz399001":
#                 df = ak.stock_zh_index_daily(symbol="sz399001")
#             elif index_code == "sz399006":
#                 df = ak.stock_zh_index_daily(symbol="sz399006")
#             else:
#                 print(f"暂不支持该指数: {index_code}")
#                 return None
                
#             # 转换日期格式并筛选数据
#             df['date'] = pd.to_datetime(df['date'])
#             df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
#             # 计算涨跌幅(%)
#             df['pct_change'] = df['close'].pct_change() * 100
            
#             return df
#         except Exception as e:
#             print(f"获取指数数据时出错: {e}")
#             return None
    
#     def get_north_flow_data(self, start_date, end_date):
#         """获取北向资金净流入数据（兼容多种akshare版本）"""
#         try:
#             # 尝试最新接口
#             try:
#                 df = ak.stock_hsgt_north_net_flow_in_em()
#                 if df is None or df.empty:
#                     raise Exception("获取北向资金数据失败")
                    
#                 df['date'] = pd.to_datetime(df['date'])
#                 df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                 df = df.rename(columns={'net_amount': 'north_net_inflow'})
#                 # 转换为亿元单位
#                 df['north_net_inflow'] = df['north_net_inflow'] / 100000000
#                 return df[['date', 'north_net_inflow']]
#             except Exception as e1:
#                 print(f"尝试最新北向资金接口失败: {e1}")
                
#                 # 尝试旧接口
#                 try:
#                     df = ak.stock_individual_fund_flow_rank()
#                     if df is None or df.empty:
#                         raise Exception("获取北向资金数据失败")
                        
#                     df['date'] = pd.to_datetime(df['日期'])
#                     df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                     df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
#                     return df[['date', 'north_net_inflow']]
#                 except Exception as e2:
#                     print(f"尝试旧北向资金接口失败: {e2}")
                    
#                     # 尝试备选接口
#                     try:
#                         df = ak.stock_market_fund_flow()
#                         if df is None or df.empty:
#                             raise Exception("获取北向资金数据失败")
                            
#                         df['date'] = pd.to_datetime(df['日期'])
#                         df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                         df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
#                         return df[['date', 'north_net_inflow']]
#                     except Exception as e3:
#                         print(f"尝试备选北向资金接口失败: {e3}")
#                         raise Exception("无法获取北向资金数据，请确保akshare版本是最新的")
#         except Exception as e:
#             print(f"获取北向资金数据时出错: {e}")
#             return None
    
#     def get_main_money_flow_data(self, start_date, end_date):
#         """获取A股主力资金净流入数据（兼容多种akshare版本）"""
#         try:
#             # 尝试使用stock_market_fund_flow接口（新方法）
#             try:
#                 df = ak.stock_market_fund_flow()
#                 if df is None or df.empty:
#                     raise Exception("获取大盘资金流向数据失败")
                    
#                 df['date'] = pd.to_datetime(df['日期'])
#                 df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                 df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
                
#                 # 检查数据是否包含有效内容
#                 if 'main_net_inflow' in df.columns and not df['main_net_inflow'].isna().all():
#                     # 转换单位为亿元（根据数据实际情况判断是否需要转换）
#                     if df['main_net_inflow'].abs().max() > 10000:  # 如果数值超过1亿，认为是元单位
#                         df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                     return df[['date', 'main_net_inflow']]
#                 else:
#                     raise Exception("主力资金数据格式异常")
#             except Exception as e1:
#                 print(f"尝试大盘资金流向接口失败: {e1}")
                
#                 # 尝试使用北向资金数据作为主力资金的替代
#                 try:
#                     df = ak.stock_hsgt_north_net_flow_in_daily()
#                     if df is None or df.empty:
#                         raise Exception("获取北向资金数据失败")
                        
#                     df['date'] = pd.to_datetime(df['date'])
#                     df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                     df = df.rename(columns={'net_amount': 'main_net_inflow'})
#                     # 转换为亿元单位
#                     df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                     return df[['date', 'main_net_inflow']]
#                 except Exception as e2:
#                     print(f"尝试北向资金接口失败: {e2}")
                    
#                     # 尝试使用stock_individual_fund_flow接口
#                     try:
#                         df = ak.stock_individual_fund_flow(stock="all")
#                         if df is None or df.empty:
#                             raise Exception("获取个股资金流向数据失败")
                            
#                         # 检查是否包含必要的列
#                         if '日期' not in df.columns or '主力净流入-净额' not in df.columns:
#                             print(f"个股资金流向数据格式异常: {df.columns}")
#                             raise Exception("个股资金流向数据格式异常")
                            
#                         # 按日期分组并计算主力资金净流入总和
#                         df['date'] = pd.to_datetime(df['日期'])
#                         df = df.groupby('date')['主力净流入-净额'].sum().reset_index()
#                         df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
#                         # 筛选日期范围
#                         df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                        
#                         # 检查数据是否包含有效内容
#                         if 'main_net_inflow' in df.columns and not df['main_net_inflow'].isna().all():
#                             # 转换单位为亿元（根据数据实际情况判断是否需要转换）
#                             if df['main_net_inflow'].abs().max() > 10000:  # 如果数值超过1亿，认为是元单位
#                                 df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                             return df
#                         else:
#                             raise Exception("主力资金数据无有效内容")
#                     except Exception as e3:
#                         print(f"尝试个股资金流向接口失败: {e3}")
#                         raise Exception("无法获取主力资金数据，请确保akshare版本是最新的")
#         except Exception as e:
#             print(f"获取主力资金数据时出错: {e}")
#             return None
    
#     def merge_data(self, index_data, north_data, main_data, analyze_north):
#         """合并各类数据（支持北向资金开关）"""
#         try:
#             # 初始化合并数据
#             merged_data = pd.merge(main_data, index_data[['date', 'close', 'pct_change']], 
#                                   on='date', how='outer')
            
#             # 如果关注北向资金，添加北向数据
#             if analyze_north and north_data is not None and not north_data.empty:
#                 merged_data = pd.merge(merged_data, north_data[['date', 'north_net_inflow']], 
#                                       on='date', how='outer')
            
#             # 按日期排序并填充缺失值
#             merged_data = merged_data.sort_values('date')
#             merged_data = merged_data.ffill()  # 修复FutureWarning
            
#             return merged_data
#         except Exception as e:
#             print(f"合并数据时出错: {e}")
#             return None
    
#     def calculate_correlations(self, data, analyze_north):
#         """计算相关系数（根据北向开关过滤计算项）"""
#         if data is None or data.empty:
#             return None
        
#         correlations = {}
        
#         # 主力资金与指数涨跌幅的相关系数
#         if 'main_net_inflow' in data.columns and 'pct_change' in data.columns:
#             correlations['main'] = data['main_net_inflow'].corr(data['pct_change'])
        
#         # 北向资金相关系数仅在关注时计算
#         if analyze_north:
#             if 'north_net_inflow' in data.columns and 'pct_change' in data.columns:
#                 correlations['north'] = data['north_net_inflow'].corr(data['pct_change'])
            
#             if 'north_net_inflow' in data.columns and 'main_net_inflow' in data.columns:
#                 correlations['fund'] = data['north_net_inflow'].corr(data['main_net_inflow'])
        
#         return correlations
    
#     def update_results(self, data, index_name, correlations, analyze_north):
#         """更新结果显示（根据北向开关控制显示内容）"""
#         # 更新概览卡片
#         self.update_overview_cards(correlations, analyze_north)
        
#         # 绘制趋势图
#         self.draw_trend_chart(data, index_name, analyze_north)
        
#         # 绘制散点图
#         self.draw_scatter_chart(data, index_name, analyze_north)
        
#         # 更新数据表格
#         self.update_data_table(data, analyze_north)
    
#     def update_overview_cards(self, correlations, analyze_north):
#         """根据北向开关更新概览卡片显示"""
#         # 主力资金相关性
#         self.main_value.set(f"{correlations.get('main', '--'):.2f}")
        
#         if analyze_north:
#             # 显示北向相关卡片
#             self.north_card.grid()
#             self.fund_card.grid()
#             self.main_card.grid_configure(column=1)
            
#             self.north_value.set(f"{correlations.get('north', '--'):.2f}")
#             self.fund_value.set(f"{correlations.get('fund', '--'):.2f}")
#         else:
#             # 隐藏北向相关卡片
#             self.north_card.grid_remove()
#             self.fund_card.grid_remove()
#             self.main_card.grid_configure(column=0, columnspan=3)
        
#         # 确保布局正确
#         self.overview_frame.update_idletasks()
    
#     def draw_trend_chart(self, data, index_name, analyze_north):
#         """绘制趋势图"""
#         self.trend_ax.clear()
#         dates = data['date'].dt.strftime('%Y-%m-%d')
        
#         # 绘制指数曲线
#         self.trend_ax.plot(dates, data['close'], 'b-', label='指数收盘价')
#         self.trend_ax.set_ylabel('指数收盘价', color='b')
#         self.trend_ax.tick_params(axis='y', labelcolor='b')
        
#         ax2 = self.trend_ax.twinx()
        
#         # 绘制主力资金柱状图
#         bar_width = 0.35
#         main_bars = ax2.bar(dates, data['main_net_inflow'], width=bar_width, alpha=0.5, color='g', label='主力资金净流入')
        
#         # 绘制北向资金柱状图（如果关注）
#         if analyze_north and 'north_net_inflow' in data.columns:
#             north_bars = ax2.bar([x + bar_width for x in range(len(dates))], data['north_net_inflow'], 
#                                width=bar_width, alpha=0.5, color='r', label='北向资金净流入')
        
#         ax2.set_ylabel('资金净流入(亿)', color='k')
#         ax2.tick_params(axis='y', labelcolor='k')
        
#         # 生成图例
#         handles, labels = self.trend_ax.get_legend_handles_labels()
#         handles.append(main_bars[0])
#         labels.append('主力资金净流入')
#         if analyze_north:
#             handles.append(plt.Rectangle((0,0),1,1,fc='r', alpha=0.5))
#             labels.append('北向资金净流入')
        
#         ax2.legend(handles, labels, loc='upper left')
        
#         self.trend_ax.set_title(f'{index_name}与资金流向趋势图')
#         self.trend_ax.set_xticks(range(len(dates)))
#         self.trend_ax.set_xticklabels(dates, rotation=45, ha='right')
#         self.trend_fig.tight_layout()
#         self.trend_canvas.draw()
    
#     def draw_scatter_chart(self, data, index_name, analyze_north):
#         """绘制散点图"""
#         self.scatter_ax.clear()
        
#         # 主力资金散点
#         self.scatter_ax.scatter(data['main_net_inflow'], data['pct_change'], c='g', alpha=0.5, label='主力资金')
        
#         # 北向资金散点（如果关注）
#         if analyze_north and 'north_net_inflow' in data.columns:
#             self.scatter_ax.scatter(data['north_net_inflow'], data['pct_change'], c='r', alpha=0.5, label='北向资金')
        
#         self.scatter_ax.set_xlabel('资金净流入(亿)')
#         self.scatter_ax.set_ylabel('涨跌幅(%)')
#         self.scatter_ax.set_title(f'资金净流入与{index_name}涨跌幅关系')
#         self.scatter_ax.legend()
#         self.scatter_fig.tight_layout()
#         self.scatter_canvas.draw()
    
#     def update_data_table(self, data, analyze_north):
#         """根据北向开关更新数据表格列"""
#         # 定义列
#         columns = ("日期", "指数收盘价", "涨跌幅(%)", "主力资金净流入(亿)")
#         if analyze_north and 'north_net_inflow' in data.columns:
#             columns += ("北向资金净流入(亿)",)
        
#         # 更新列配置
#         self.data_tree['columns'] = columns
#         for col in columns:
#             self.data_tree.heading(col, text=col)
#             self.data_tree.column(col, width=150, anchor=tk.CENTER)
        
#         # 清空数据
#         for item in self.data_tree.get_children():
#             self.data_tree.delete(item)
        
#         # 填充数据
#         for i, row in data.iterrows():
#             values = [
#                 row['date'].strftime('%Y-%m-%d'),
#                 f"{row['close']:.2f}",
#                 f"{row['pct_change']:.2f}",
#                 f"{row['main_net_inflow']:.2f}"
#             ]
#             if analyze_north:
#                 values.append(f"{row.get('north_net_inflow', '--'):.2f}")
            
#             self.data_tree.insert("", "end", values=values)
    
#     def export_data(self):
#         """导出数据到CSV文件"""
#         if self.current_data is None or self.current_data.empty:
#             messagebox.showinfo("导出数据", "没有数据可导出")
#             return
        
#         from tkinter import filedialog
        
#         # 获取保存路径
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".csv",
#             filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
#             title="保存数据"
#         )
        
#         if not file_path:
#             return
        
#         try:
#             # 保存数据
#             self.current_data.to_csv(file_path, index=False, encoding='utf-8-sig')
#             messagebox.showinfo("导出成功", f"数据已成功导出到 {file_path}")
#         except Exception as e:
#             messagebox.showerror("导出失败", f"导出数据时出错: {str(e)}")

# def main():
#     root = tk.Tk()
#     app = StockAnalysisApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()


# import akshare as ak
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime, timedelta
# import tkinter as tk
# from tkinter import ttk, messagebox, scrolledtext
# import matplotlib
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# import numpy as np
# import threading
# import re

# # 设置中文字体
# matplotlib.use("TkAgg")
# plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
# plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# class DatePicker(ttk.Frame):
#     """日期选择器组件"""
#     def __init__(self, parent, default_date=None):
#         super().__init__(parent)
#         self.parent = parent
        
#         # 如果没有提供默认日期，使用今天的日期
#         if default_date:
#             self.date_var = tk.StringVar(value=default_date.strftime('%Y-%m-%d'))
#         else:
#             self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        
#         # 创建日期输入框
#         self.date_entry = ttk.Entry(self, textvariable=self.date_var, width=12)
#         self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
#         # 创建日期选择按钮
#         self.date_btn = ttk.Button(self, text="??", command=self.select_date)
#         self.date_btn.pack(side=tk.LEFT)
    
#     def get_date(self):
#         """获取选择的日期"""
#         try:
#             return datetime.strptime(self.date_var.get(), '%Y-%m-%d')
#         except ValueError:
#             messagebox.showerror("日期格式错误", "请使用YYYY-MM-DD格式的日期")
#             return None
    
#     def select_date(self):
#         """打开日期选择对话框"""
#         # 这里使用简单的输入对话框，实际应用中可以使用更高级的日期选择器
#         from tkinter import simpledialog
        
#         current_date = self.date_var.get()
#         new_date = simpledialog.askstring("选择日期", "请输入日期 (YYYY-MM-DD):", 
#                                          initialvalue=current_date)
        
#         if new_date:
#             try:
#                 # 验证日期格式
#                 datetime.strptime(new_date, '%Y-%m-%d')
#                 self.date_var.set(new_date)
#             except ValueError:
#                 messagebox.showerror("日期格式错误", "请使用YYYY-MM-DD格式的日期")

# class StockAnalysisApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("A股资金流向与指数关系分析")
#         self.root.geometry("1200x800")
#         self.root.minsize(1000, 700)
        
#         # 数据缓存
#         self.current_data = None
        
#         # 北向资金开关
#         self.north_enabled = tk.BooleanVar(value=False)
        
#         # 创建界面
#         self.create_widgets()
        
#         # 检查akshare版本
#         self.check_akshare_version()
        
#     def check_akshare_version(self):
#         """检查akshare版本并显示提示"""
#         try:
#             version = ak.__version__
#             self.status_var.set(f"已加载 akshare v{version}")
#             # 检查是否为较新版本
#             major, minor, _ = map(int, re.findall(r'\d+', version)[:3])
#             if major < 1 or (major == 1 and minor < 30):
#                 messagebox.showinfo("版本提示", 
#                     f"您的akshare版本为{version}，建议升级到最新版本以获取最佳兼容性。\n"
#                     "可通过命令: 'pip install akshare --upgrade' 进行升级。")
#         except Exception as e:
#             print(f"检查akshare版本时出错: {e}")
#             self.status_var.set("无法确定akshare版本，请确保已安装最新版本")
    
#     def create_widgets(self):
#         # 创建主框架
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # 控制面板
#         control_frame = ttk.LabelFrame(main_frame, text="分析参数设置", padding="10")
#         control_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # 指数选择
#         ttk.Label(control_frame, text="选择指数:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
#         self.index_var = tk.StringVar(value="sh000001")
#         index_frame = ttk.Frame(control_frame)
#         index_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
#         index_options = [
#             ("上证指数", "sh000001"),
#             ("深证成指", "sz399001"),
#             ("创业板指", "sz399006"),
#             ("科创50", "sh000688"),  # 新增科创50指数
#             ("沪深300", "sh000300")   # 新增沪深300指数
#         ]
        
#         # 动态计算每行显示的指数选项数量
#         options_per_row = 3
#         for i, (text, value) in enumerate(index_options):
#             row = i // options_per_row
#             col = i % options_per_row
#             ttk.Radiobutton(index_frame, text=text, variable=self.index_var, value=value).grid(row=row, column=col, padx=10, pady=5)
        
#         # 日期选择
#         ttk.Label(control_frame, text="开始日期:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
#         self.start_date_picker = DatePicker(control_frame, datetime.now() - timedelta(days=30))
#         self.start_date_picker.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
#         ttk.Label(control_frame, text="结束日期:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
#         self.end_date_picker = DatePicker(control_frame, datetime.now())
#         self.end_date_picker.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
#         # 资金类型选择
#         ttk.Label(control_frame, text="关注资金:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
#         fund_frame = ttk.Frame(control_frame)
#         fund_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
#         self.north_check = ttk.Checkbutton(fund_frame, text="北向资金", variable=self.north_enabled)
#         self.north_check.grid(row=0, column=0, padx=5)
#         self.main_check = ttk.Checkbutton(fund_frame, text="主力资金", variable=tk.BooleanVar(value=True))
#         self.main_check.grid(row=0, column=1, padx=5)
        
#         # 分析按钮
#         self.analyze_btn = ttk.Button(control_frame, text="开始分析", command=self.start_analysis)
#         self.analyze_btn.grid(row=0, column=2, rowspan=5, padx=20, pady=5, sticky=tk.EW)
        
#         # 状态栏
#         self.status_var = tk.StringVar(value="就绪")
#         self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
#         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
#         # 结果区域 - 使用Notebook创建选项卡
#         self.notebook = ttk.Notebook(main_frame)
#         self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
#         # 概览选项卡
#         self.overview_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.overview_frame, text="分析概览")
        
#         # 趋势图选项卡
#         self.trend_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.trend_frame, text="资金与指数趋势")
        
#         # 散点图选项卡
#         self.scatter_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.scatter_frame, text="相关性分析")
        
#         # 数据表格选项卡
#         self.data_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.data_frame, text="详细数据")
        
#         # 创建趋势图
#         self.trend_fig = Figure(figsize=(10, 5), dpi=100)
#         self.trend_ax = self.trend_fig.add_subplot(111)
#         self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, master=self.trend_frame)
#         self.trend_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
#         # 创建散点图
#         self.scatter_fig = Figure(figsize=(10, 5), dpi=100)
#         self.scatter_ax = self.scatter_fig.add_subplot(111)
#         self.scatter_canvas = FigureCanvasTkAgg(self.scatter_fig, master=self.scatter_frame)
#         self.scatter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
#         # 创建数据表格
#         self.data_tree = ttk.Treeview(self.data_frame)
#         scrollbar = ttk.Scrollbar(self.data_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
#         self.data_tree.configure(yscroll=scrollbar.set)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.data_tree.pack(fill=tk.BOTH, expand=True)
        
#         # 导出按钮
#         self.export_btn = ttk.Button(self.data_frame, text="导出数据", command=self.export_data)
#         self.export_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
#         # 创建概览卡片
#         self.create_overview_cards()
    
#     def create_overview_cards(self):
#         # 初始卡片布局
#         self.north_card = ttk.LabelFrame(self.overview_frame, text="北向资金相关性", padding="10")
#         self.north_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
#         self.north_card.grid_remove()
        
#         self.main_card = ttk.LabelFrame(self.overview_frame, text="主力资金相关性", padding="10")
#         self.main_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        
#         self.fund_card = ttk.LabelFrame(self.overview_frame, text="资金协同性", padding="10")
#         self.fund_card.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)
#         self.fund_card.grid_remove()
        
#         self.north_value = tk.StringVar(value="--")
#         ttk.Label(self.north_card, textvariable=self.north_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.north_card, text="北向资金净流入与指数涨跌幅的相关系数").pack()
        
#         self.main_value = tk.StringVar(value="--")
#         ttk.Label(self.main_card, textvariable=self.main_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.main_card, text="主力资金净流入与指数涨跌幅的相关系数").pack()
        
#         self.fund_value = tk.StringVar(value="--")
#         ttk.Label(self.fund_card, textvariable=self.fund_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.fund_card, text="北向资金与主力资金的协同系数").pack()
        
#         # 设置列权重
#         self.overview_frame.grid_columnconfigure(0, weight=1)
#         self.overview_frame.grid_columnconfigure(1, weight=1)
#         self.overview_frame.grid_columnconfigure(2, weight=1)
    
#     def start_analysis(self):
#         """开始分析"""
#         # 禁用按钮
#         self.analyze_btn.config(state=tk.DISABLED)
#         self.status_var.set("正在获取数据...")
        
#         # 获取日期
#         start_date = self.start_date_picker.get_date()
#         end_date = self.end_date_picker.get_date()
        
#         # 验证日期
#         if not start_date or not end_date:
#             self.status_var.set("日期格式错误")
#             self.analyze_btn.config(state=tk.NORMAL)
#             return
        
#         if start_date >= end_date:
#             messagebox.showerror("日期错误", "开始日期必须早于结束日期")
#             self.status_var.set("就绪")
#             self.analyze_btn.config(state=tk.NORMAL)
#             return
        
#         # 在单独的线程中执行分析，避免阻塞UI
#         analysis_thread = threading.Thread(target=self.perform_analysis, args=(start_date, end_date))
#         analysis_thread.daemon = True
#         analysis_thread.start()
    
#     def perform_analysis(self, start_date, end_date):
#         try:
#             # 获取参数
#             index_code = self.index_var.get()
#             analyze_north = self.north_enabled.get()
#             analyze_main = True
            
#             # 获取指数名称
#             index_names = {
#                 "sh000001": "上证指数",
#                 "sz399001": "深证成指",
#                 "sz399006": "创业板指",
#                 "sh000688": "科创50",  # 新增科创50指数名称
#                 "sh000300": "沪深300"   # 新增沪深300指数名称
#             }
#             index_name = index_names.get(index_code, "未知指数")
            
#             # 更新状态
#             self.update_status(f"正在获取{index_name}数据...")
            
#             # 获取数据
#             index_data = self.get_market_index_data(index_code, start_date, end_date)
#             if index_data is None or index_data.empty:
#                 raise Exception(f"无法获取{index_name}数据")
            
#             north_data = None
#             if analyze_north:
#                 self.update_status("正在获取北向资金数据...")
#                 north_data = self.get_north_flow_data(start_date, end_date)
#                 if north_data is None or north_data.empty:
#                     raise Exception("无法获取北向资金数据")
            
#             self.update_status("正在获取主力资金数据...")
#             main_data = self.get_main_money_flow_data(start_date, end_date)
#             if main_data is None or main_data.empty:
#                 raise Exception("无法获取主力资金数据")
            
#             self.update_status("正在合并和分析数据...")
            
#             # 合并数据
#             merged_data = self.merge_data(index_data, north_data, main_data, analyze_north)
#             if merged_data is None or merged_data.empty:
#                 raise Exception("合并数据失败")
            
#             # 保存当前数据
#             self.current_data = merged_data
            
#             # 计算相关系数
#             correlations = self.calculate_correlations(merged_data, analyze_north)
            
#             # 更新UI
#             self.root.after(0, lambda: self.update_results(merged_data, index_name, correlations, analyze_north))
            
#             self.update_status("分析完成")
#         except Exception as e:
#             # 显示错误信息
#             self.root.after(0, lambda: messagebox.showerror("分析错误", str(e)))
#             self.update_status("分析失败")
#         finally:
#             # 重新启用按钮
#             self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
    
#     def update_status(self, message):
#         """更新状态栏"""
#         self.status_var.set(message)
#         self.root.update_idletasks()
    
#     def get_market_index_data(self, index_code, start_date, end_date):
#         """获取指定指数的历史数据"""
#         try:
#             # 特殊处理科创50和沪深300指数
#             if index_code == "sh000688":  # 科创50
#                 df = ak.stock_zh_index_daily(symbol="sh000688")
#             elif index_code == "sh000300":  # 沪深300
#                 df = ak.stock_zh_index_daily(symbol="sh000300")
#             elif index_code == "sh000001":
#                 df = ak.stock_zh_index_daily(symbol="sh000001")
#             elif index_code == "sz399001":
#                 df = ak.stock_zh_index_daily(symbol="sz399001")
#             elif index_code == "sz399006":
#                 df = ak.stock_zh_index_daily(symbol="sz399006")
#             else:
#                 print(f"暂不支持该指数: {index_code}")
#                 return None
                
#             # 转换日期格式并筛选数据
#             df['date'] = pd.to_datetime(df['date'])
#             df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
#             # 计算涨跌幅(%)
#             df['pct_change'] = df['close'].pct_change() * 100
            
#             return df
#         except Exception as e:
#             print(f"获取指数数据时出错: {e}")
#             return None
    
#     def get_north_flow_data(self, start_date, end_date):
#         """获取北向资金净流入数据（兼容多种akshare版本）"""
#         try:
#             # 尝试最新接口
#             try:
#                 df = ak.stock_hsgt_north_net_flow_in_em()
#                 if df is None or df.empty:
#                     raise Exception("获取北向资金数据失败")
                    
#                 df['date'] = pd.to_datetime(df['date'])
#                 df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                 df = df.rename(columns={'net_amount': 'north_net_inflow'})
#                 # 转换为亿元单位
#                 df['north_net_inflow'] = df['north_net_inflow'] / 100000000
#                 return df[['date', 'north_net_inflow']]
#             except Exception as e1:
#                 print(f"尝试最新北向资金接口失败: {e1}")
                
#                 # 尝试旧接口
#                 try:
#                     df = ak.stock_individual_fund_flow_rank()
#                     if df is None or df.empty:
#                         raise Exception("获取北向资金数据失败")
                        
#                     df['date'] = pd.to_datetime(df['日期'])
#                     df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                     df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
#                     return df[['date', 'north_net_inflow']]
#                 except Exception as e2:
#                     print(f"尝试旧北向资金接口失败: {e2}")
                    
#                     # 尝试备选接口
#                     try:
#                         df = ak.stock_market_fund_flow()
#                         if df is None or df.empty:
#                             raise Exception("获取北向资金数据失败")
                            
#                         df['date'] = pd.to_datetime(df['日期'])
#                         df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                         df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
#                         return df[['date', 'north_net_inflow']]
#                     except Exception as e3:
#                         print(f"尝试备选北向资金接口失败: {e3}")
#                         raise Exception("无法获取北向资金数据，请确保akshare版本是最新的")
#         except Exception as e:
#             print(f"获取北向资金数据时出错: {e}")
#             return None
    
#     def get_main_money_flow_data(self, start_date, end_date):
#         """获取A股主力资金净流入数据（兼容多种akshare版本）"""
#         try:
#             # 尝试使用stock_market_fund_flow接口（新方法）
#             try:
#                 df = ak.stock_market_fund_flow()
#                 if df is None or df.empty:
#                     raise Exception("获取大盘资金流向数据失败")
                    
#                 df['date'] = pd.to_datetime(df['日期'])
#                 df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                 df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
                
#                 # 检查数据是否包含有效内容
#                 if 'main_net_inflow' in df.columns and not df['main_net_inflow'].isna().all():
#                     # 转换单位为亿元（根据数据实际情况判断是否需要转换）
#                     if df['main_net_inflow'].abs().max() > 10000:  # 如果数值超过1亿，认为是元单位
#                         df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                     return df[['date', 'main_net_inflow']]
#                 else:
#                     raise Exception("主力资金数据格式异常")
#             except Exception as e1:
#                 print(f"尝试大盘资金流向接口失败: {e1}")
                
#                 # 尝试使用北向资金数据作为主力资金的替代
#                 try:
#                     df = ak.stock_hsgt_north_net_flow_in_daily()
#                     if df is None or df.empty:
#                         raise Exception("获取北向资金数据失败")
                        
#                     df['date'] = pd.to_datetime(df['date'])
#                     df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                     df = df.rename(columns={'net_amount': 'main_net_inflow'})
#                     # 转换为亿元单位
#                     df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                     return df[['date', 'main_net_inflow']]
#                 except Exception as e2:
#                     print(f"尝试北向资金接口失败: {e2}")
                    
#                     # 尝试使用stock_individual_fund_flow接口
#                     try:
#                         df = ak.stock_individual_fund_flow(stock="all")
#                         if df is None or df.empty:
#                             raise Exception("获取个股资金流向数据失败")
                            
#                         # 检查是否包含必要的列
#                         if '日期' not in df.columns or '主力净流入-净额' not in df.columns:
#                             print(f"个股资金流向数据格式异常: {df.columns}")
#                             raise Exception("个股资金流向数据格式异常")
                            
#                         # 按日期分组并计算主力资金净流入总和
#                         df['date'] = pd.to_datetime(df['日期'])
#                         df = df.groupby('date')['主力净流入-净额'].sum().reset_index()
#                         df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
#                         # 筛选日期范围
#                         df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                        
#                         # 检查数据是否包含有效内容
#                         if 'main_net_inflow' in df.columns and not df['main_net_inflow'].isna().all():
#                             # 转换单位为亿元（根据数据实际情况判断是否需要转换）
#                             if df['main_net_inflow'].abs().max() > 10000:  # 如果数值超过1亿，认为是元单位
#                                 df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                             return df
#                         else:
#                             raise Exception("主力资金数据无有效内容")
#                     except Exception as e3:
#                         print(f"尝试个股资金流向接口失败: {e3}")
#                         raise Exception("无法获取主力资金数据，请确保akshare版本是最新的")
#         except Exception as e:
#             print(f"获取主力资金数据时出错: {e}")
#             return None
    
#     def merge_data(self, index_data, north_data, main_data, analyze_north):
#         """合并各类数据（支持北向资金开关）"""
#         try:
#             # 初始化合并数据
#             merged_data = pd.merge(main_data, index_data[['date', 'close', 'pct_change']], 
#                                   on='date', how='outer')
            
#             # 如果关注北向资金，添加北向数据
#             if analyze_north and north_data is not None and not north_data.empty:
#                 merged_data = pd.merge(merged_data, north_data[['date', 'north_net_inflow']], 
#                                       on='date', how='outer')
            
#             # 按日期排序并填充缺失值
#             merged_data = merged_data.sort_values('date')
#             merged_data = merged_data.ffill()  # 修复FutureWarning
            
#             return merged_data
#         except Exception as e:
#             print(f"合并数据时出错: {e}")
#             return None
    
#     def calculate_correlations(self, data, analyze_north):
#         """计算相关系数（根据北向开关过滤计算项）"""
#         if data is None or data.empty:
#             return None
        
#         correlations = {}
        
#         # 主力资金与指数涨跌幅的相关系数
#         if 'main_net_inflow' in data.columns and 'pct_change' in data.columns:
#             correlations['main'] = data['main_net_inflow'].corr(data['pct_change'])
        
#         # 北向资金相关系数仅在关注时计算
#         if analyze_north:
#             if 'north_net_inflow' in data.columns and 'pct_change' in data.columns:
#                 correlations['north'] = data['north_net_inflow'].corr(data['pct_change'])
            
#             if 'north_net_inflow' in data.columns and 'main_net_inflow' in data.columns:
#                 correlations['fund'] = data['north_net_inflow'].corr(data['main_net_inflow'])
        
#         return correlations
    
#     def update_results(self, data, index_name, correlations, analyze_north):
#         """更新结果显示（根据北向开关控制显示内容）"""
#         # 更新概览卡片
#         self.update_overview_cards(correlations, analyze_north)
        
#         # 绘制趋势图
#         self.draw_trend_chart(data, index_name, analyze_north)
        
#         # 绘制散点图
#         self.draw_scatter_chart(data, index_name, analyze_north)
        
#         # 更新数据表格
#         self.update_data_table(data, analyze_north)
    
#     def update_overview_cards(self, correlations, analyze_north):
#         """根据北向开关更新概览卡片显示"""
#         # 主力资金相关性
#         self.main_value.set(f"{correlations.get('main', '--'):.2f}")
        
#         if analyze_north:
#             # 显示北向相关卡片
#             self.north_card.grid()
#             self.fund_card.grid()
#             self.main_card.grid_configure(column=1)
            
#             self.north_value.set(f"{correlations.get('north', '--'):.2f}")
#             self.fund_value.set(f"{correlations.get('fund', '--'):.2f}")
#         else:
#             # 隐藏北向相关卡片
#             self.north_card.grid_remove()
#             self.fund_card.grid_remove()
#             self.main_card.grid_configure(column=0, columnspan=3)
        
#         # 确保布局正确
#         self.overview_frame.update_idletasks()
    
#     def draw_trend_chart(self, data, index_name, analyze_north):
#         """绘制趋势图"""
#         self.trend_ax.clear()
#         dates = data['date'].dt.strftime('%Y-%m-%d')
        
#         # 绘制指数曲线
#         self.trend_ax.plot(dates, data['close'], 'b-', label='指数收盘价')
#         self.trend_ax.set_ylabel('指数收盘价', color='b')
#         self.trend_ax.tick_params(axis='y', labelcolor='b')
        
#         ax2 = self.trend_ax.twinx()
        
#         # 绘制主力资金柱状图
#         bar_width = 0.35
#         main_bars = ax2.bar(dates, data['main_net_inflow'], width=bar_width, alpha=0.5, color='g', label='主力资金净流入')
        
#         # 绘制北向资金柱状图（如果关注）
#         if analyze_north and 'north_net_inflow' in data.columns:
#             north_bars = ax2.bar([x + bar_width for x in range(len(dates))], data['north_net_inflow'], 
#                                width=bar_width, alpha=0.5, color='r', label='北向资金净流入')
        
#         ax2.set_ylabel('资金净流入(亿)', color='k')
#         ax2.tick_params(axis='y', labelcolor='k')
        
#         # 生成图例
#         handles, labels = self.trend_ax.get_legend_handles_labels()
#         handles.append(main_bars[0])
#         labels.append('主力资金净流入')
#         if analyze_north:
#             handles.append(plt.Rectangle((0,0),1,1,fc='r', alpha=0.5))
#             labels.append('北向资金净流入')
        
#         ax2.legend(handles, labels, loc='upper left')
        
#         self.trend_ax.set_title(f'{index_name}与资金流向趋势图')
#         self.trend_ax.set_xticks(range(len(dates)))
#         self.trend_ax.set_xticklabels(dates, rotation=45, ha='right')
#         self.trend_fig.tight_layout()
#         self.trend_canvas.draw()
    
#     def draw_scatter_chart(self, data, index_name, analyze_north):
#         """绘制散点图"""
#         self.scatter_ax.clear()
        
#         # 主力资金散点
#         self.scatter_ax.scatter(data['main_net_inflow'], data['pct_change'], c='g', alpha=0.5, label='主力资金')
        
#         # 北向资金散点（如果关注）
#         if analyze_north and 'north_net_inflow' in data.columns:
#             self.scatter_ax.scatter(data['north_net_inflow'], data['pct_change'], c='r', alpha=0.5, label='北向资金')
        
#         self.scatter_ax.set_xlabel('资金净流入(亿)')
#         self.scatter_ax.set_ylabel('涨跌幅(%)')
#         self.scatter_ax.set_title(f'资金净流入与{index_name}涨跌幅关系')
#         self.scatter_ax.legend()
#         self.scatter_fig.tight_layout()
#         self.scatter_canvas.draw()
    
#     def update_data_table(self, data, analyze_north):
#         """根据北向开关更新数据表格列"""
#         # 定义列
#         columns = ("日期", "指数收盘价", "涨跌幅(%)", "主力资金净流入(亿)")
#         if analyze_north and 'north_net_inflow' in data.columns:
#             columns += ("北向资金净流入(亿)",)
        
#         # 更新列配置
#         self.data_tree['columns'] = columns
#         for col in columns:
#             self.data_tree.heading(col, text=col)
#             self.data_tree.column(col, width=150, anchor=tk.CENTER)
        
#         # 清空数据
#         for item in self.data_tree.get_children():
#             self.data_tree.delete(item)
        
#         # 填充数据
#         for i, row in data.iterrows():
#             values = [
#                 row['date'].strftime('%Y-%m-%d'),
#                 f"{row['close']:.2f}",
#                 f"{row['pct_change']:.2f}",
#                 f"{row['main_net_inflow']:.2f}"
#             ]
#             if analyze_north:
#                 values.append(f"{row.get('north_net_inflow', '--'):.2f}")
            
#             self.data_tree.insert("", "end", values=values)
    
#     def export_data(self):
#         """导出数据到CSV文件"""
#         if self.current_data is None or self.current_data.empty:
#             messagebox.showinfo("导出数据", "没有数据可导出")
#             return
        
#         from tkinter import filedialog
        
#         # 获取保存路径
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".csv",
#             filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
#             title="保存数据"
#         )
        
#         if not file_path:
#             return
        
#         try:
#             # 保存数据
#             self.current_data.to_csv(file_path, index=False, encoding='utf-8-sig')
#             messagebox.showinfo("导出成功", f"数据已成功导出到 {file_path}")
#         except Exception as e:
#             messagebox.showerror("导出失败", f"导出数据时出错: {str(e)}")

# def main():
#     root = tk.Tk()
#     app = StockAnalysisApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()


# import akshare as ak
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime, timedelta
# import tkinter as tk
# from tkinter import ttk, messagebox, scrolledtext
# import matplotlib
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# import numpy as np
# import threading
# import re
# from tkcalendar import Calendar, DateEntry  # 导入日历组件

# # 设置中文字体
# matplotlib.use("TkAgg")
# plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
# plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# class DatePicker(ttk.Frame):
#     """日期选择器组件"""
#     def __init__(self, parent, default_date=None):
#         super().__init__(parent)
#         self.parent = parent
        
#         # 如果没有提供默认日期，使用今天的日期
#         if default_date:
#             self.date_var = tk.StringVar(value=default_date.strftime('%Y-%m-%d'))
#         else:
#             self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        
#         # 创建日期输入框
#         self.date_entry = DateEntry(
#             self, 
#             textvariable=self.date_var, 
#             width=12, 
#             date_pattern='yyyy-mm-dd',
#             background='darkblue',
#             foreground='white',
#             borderwidth=2
#         )
#         self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
#         # 创建日期选择按钮
#         self.date_btn = ttk.Button(self, text="📅", command=self.select_date)
#         self.date_btn.pack(side=tk.LEFT)
    
#     def get_date(self):
#         """获取选择的日期"""
#         try:
#             return datetime.strptime(self.date_var.get(), '%Y-%m-%d')
#         except ValueError:
#             messagebox.showerror("日期格式错误", "请使用YYYY-MM-DD格式的日期")
#             return None
    
#     def select_date(self):
#         """打开日期选择对话框"""
#         def on_date_selected():
#             selected_date = cal.selection_get()
#             self.date_var.set(selected_date.strftime('%Y-%m-%d'))
#             top.destroy()
        
#         top = tk.Toplevel(self)
#         top.title("选择日期")
#         top.geometry("300x250")
        
#         # 创建日历控件
#         cal = Calendar(
#             top,
#             font="Arial 10",
#             selectmode='day',
#             cursor="hand1",
#             year=self.get_date().year,
#             month=self.get_date().month,
#             day=self.get_date().day
#         )
#         cal.pack(fill="both", expand=True, padx=10, pady=10)
        
#         # 创建确认按钮
#         ttk.Button(top, text="确认", command=on_date_selected).pack(pady=10)

# class StockAnalysisApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("A股资金流向与指数关系分析")
#         self.root.geometry("1200x800")
#         self.root.minsize(1000, 700)
        
#         # 数据缓存
#         self.current_data = None
        
#         # 北向资金开关
#         self.north_enabled = tk.BooleanVar(value=False)
        
#         # 创建界面
#         self.create_widgets()
        
#         # 检查akshare版本
#         self.check_akshare_version()
        
#     def check_akshare_version(self):
#         """检查akshare版本并显示提示"""
#         try:
#             version = ak.__version__
#             self.status_var.set(f"已加载 akshare v{version}")
#             # 检查是否为较新版本
#             major, minor, _ = map(int, re.findall(r'\d+', version)[:3])
#             if major < 1 or (major == 1 and minor < 30):
#                 messagebox.showinfo("版本提示", 
#                     f"您的akshare版本为{version}，建议升级到最新版本以获取最佳兼容性。\n"
#                     "可通过命令: 'pip install akshare --upgrade' 进行升级。")
#         except Exception as e:
#             print(f"检查akshare版本时出错: {e}")
#             self.status_var.set("无法确定akshare版本，请确保已安装最新版本")
    
#     def create_widgets(self):
#         # 创建主框架
#         main_frame = ttk.Frame(self.root, padding="10")
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # 控制面板
#         control_frame = ttk.LabelFrame(main_frame, text="分析参数设置", padding="10")
#         control_frame.pack(fill=tk.X, pady=(0, 10))
        
#         # 指数选择
#         ttk.Label(control_frame, text="选择指数:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
#         self.index_var = tk.StringVar(value="sh000001")
#         index_frame = ttk.Frame(control_frame)
#         index_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
#         index_options = [
#             ("上证指数", "sh000001"),
#             ("深证成指", "sz399001"),
#             ("创业板指", "sz399006"),
#             ("科创50", "sh000688"),
#             ("沪深300", "sh000300")
#         ]
        
#         # 动态计算每行显示的指数选项数量
#         options_per_row = 3
#         for i, (text, value) in enumerate(index_options):
#             row = i // options_per_row
#             col = i % options_per_row
#             ttk.Radiobutton(index_frame, text=text, variable=self.index_var, value=value).grid(row=row, column=col, padx=10, pady=5)
        
#         # 日期选择
#         ttk.Label(control_frame, text="开始日期:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
#         self.start_date_picker = DatePicker(control_frame, datetime.now() - timedelta(days=30))
#         self.start_date_picker.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
#         ttk.Label(control_frame, text="结束日期:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
#         self.end_date_picker = DatePicker(control_frame, datetime.now())
#         self.end_date_picker.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
#         # 资金类型选择
#         ttk.Label(control_frame, text="关注资金:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
#         fund_frame = ttk.Frame(control_frame)
#         fund_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
#         self.north_check = ttk.Checkbutton(fund_frame, text="北向资金", variable=self.north_enabled)
#         self.north_check.grid(row=0, column=0, padx=5)
#         self.main_check = ttk.Checkbutton(fund_frame, text="主力资金", variable=tk.BooleanVar(value=True))
#         self.main_check.grid(row=0, column=1, padx=5)
        
#         # 分析按钮
#         self.analyze_btn = ttk.Button(control_frame, text="开始分析", command=self.start_analysis)
#         self.analyze_btn.grid(row=0, column=2, rowspan=5, padx=20, pady=5, sticky=tk.EW)
        
#         # 状态栏
#         self.status_var = tk.StringVar(value="就绪")
#         self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
#         self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
#         # 结果区域 - 使用Notebook创建选项卡
#         self.notebook = ttk.Notebook(main_frame)
#         self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
#         # 概览选项卡
#         self.overview_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.overview_frame, text="分析概览")
        
#         # 趋势图选项卡
#         self.trend_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.trend_frame, text="资金与指数趋势")
        
#         # 散点图选项卡
#         self.scatter_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.scatter_frame, text="相关性分析")
        
#         # 数据表格选项卡
#         self.data_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.data_frame, text="详细数据")
        
#         # 统计信息选项卡
#         self.stats_frame = ttk.Frame(self.notebook)
#         self.notebook.add(self.stats_frame, text="统计信息")
        
#         # 创建趋势图
#         self.trend_fig = Figure(figsize=(10, 5), dpi=100)
#         self.trend_ax = self.trend_fig.add_subplot(111)
#         self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, master=self.trend_frame)
#         self.trend_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
#         # 创建散点图
#         self.scatter_fig = Figure(figsize=(10, 5), dpi=100)
#         self.scatter_ax = self.scatter_fig.add_subplot(111)
#         self.scatter_canvas = FigureCanvasTkAgg(self.scatter_fig, master=self.scatter_frame)
#         self.scatter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
#         # 创建数据表格
#         self.data_tree = ttk.Treeview(self.data_frame)
#         scrollbar = ttk.Scrollbar(self.data_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
#         self.data_tree.configure(yscroll=scrollbar.set)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.data_tree.pack(fill=tk.BOTH, expand=True)
        
#         # 导出按钮
#         self.export_btn = ttk.Button(self.data_frame, text="导出数据", command=self.export_data)
#         self.export_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
#         # 创建概览卡片
#         self.create_overview_cards()
        
#         # 创建统计信息卡片
#         self.create_stats_cards()
    
#     def create_overview_cards(self):
#         # 初始卡片布局
#         self.north_card = ttk.LabelFrame(self.overview_frame, text="北向资金相关性", padding="10")
#         self.north_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
#         self.north_card.grid_remove()
        
#         self.main_card = ttk.LabelFrame(self.overview_frame, text="主力资金相关性", padding="10")
#         self.main_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        
#         self.fund_card = ttk.LabelFrame(self.overview_frame, text="资金协同性", padding="10")
#         self.fund_card.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)
#         self.fund_card.grid_remove()
        
#         self.north_value = tk.StringVar(value="--")
#         ttk.Label(self.north_card, textvariable=self.north_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.north_card, text="北向资金净流入与指数涨跌幅的相关系数").pack()
        
#         self.main_value = tk.StringVar(value="--")
#         ttk.Label(self.main_card, textvariable=self.main_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.main_card, text="主力资金净流入与指数涨跌幅的相关系数").pack()
        
#         self.fund_value = tk.StringVar(value="--")
#         ttk.Label(self.fund_card, textvariable=self.fund_value, font=("SimHei", 24, "bold")).pack(pady=10)
#         ttk.Label(self.fund_card, text="北向资金与主力资金的协同系数").pack()
        
#         # 设置列权重
#         self.overview_frame.grid_columnconfigure(0, weight=1)
#         self.overview_frame.grid_columnconfigure(1, weight=1)
#         self.overview_frame.grid_columnconfigure(2, weight=1)
    
#     def create_stats_cards(self):
#         # 主力资金统计卡片
#         self.main_stats_card = ttk.LabelFrame(self.stats_frame, text="主力资金统计", padding="10")
#         self.main_stats_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
#         # 创建统计信息标签
#         self.max_inflow = tk.StringVar(value="最大净流入: -- 亿元")
#         self.max_outflow = tk.StringVar(value="最大净流出: -- 亿元")
#         self.avg_inflow = tk.StringVar(value="平均净流入: -- 亿元")
#         self.total_inflow = tk.StringVar(value="总净流入: -- 亿元")
        
#         ttk.Label(self.main_stats_card, textvariable=self.max_inflow, font=("SimHei", 14)).pack(anchor=tk.W, pady=5)
#         ttk.Label(self.main_stats_card, textvariable=self.max_outflow, font=("SimHei", 14)).pack(anchor=tk.W, pady=5)
#         ttk.Label(self.main_stats_card, textvariable=self.avg_inflow, font=("SimHei", 14)).pack(anchor=tk.W, pady=5)
#         ttk.Label(self.main_stats_card, textvariable=self.total_inflow, font=("SimHei", 14)).pack(anchor=tk.W, pady=5)
    
#     def start_analysis(self):
#         """开始分析"""
#         # 禁用按钮
#         self.analyze_btn.config(state=tk.DISABLED)
#         self.status_var.set("正在获取数据...")
        
#         # 获取日期
#         start_date = self.start_date_picker.get_date()
#         end_date = self.end_date_picker.get_date()
        
#         # 验证日期
#         if not start_date or not end_date:
#             self.status_var.set("日期格式错误")
#             self.analyze_btn.config(state=tk.NORMAL)
#             return
        
#         if start_date >= end_date:
#             messagebox.showerror("日期错误", "开始日期必须早于结束日期")
#             self.status_var.set("就绪")
#             self.analyze_btn.config(state=tk.NORMAL)
#             return
        
#         # 在单独的线程中执行分析，避免阻塞UI
#         analysis_thread = threading.Thread(target=self.perform_analysis, args=(start_date, end_date))
#         analysis_thread.daemon = True
#         analysis_thread.start()
    
#     def perform_analysis(self, start_date, end_date):
#         try:
#             # 获取参数
#             index_code = self.index_var.get()
#             analyze_north = self.north_enabled.get()
#             analyze_main = True
            
#             # 获取指数名称
#             index_names = {
#                 "sh000001": "上证指数",
#                 "sz399001": "深证成指",
#                 "sz399006": "创业板指",
#                 "sh000688": "科创50",
#                 "sh000300": "沪深300"
#             }
#             index_name = index_names.get(index_code, "未知指数")
            
#             # 更新状态
#             self.update_status(f"正在获取{index_name}数据...")
            
#             # 获取数据
#             index_data = self.get_market_index_data(index_code, start_date, end_date)
#             if index_data is None or index_data.empty:
#                 raise Exception(f"无法获取{index_name}数据")
            
#             north_data = None
#             if analyze_north:
#                 self.update_status("正在获取北向资金数据...")
#                 north_data = self.get_north_flow_data(start_date, end_date)
#                 if north_data is None or north_data.empty:
#                     raise Exception("无法获取北向资金数据")
            
#             self.update_status("正在获取主力资金数据...")
#             main_data = self.get_main_money_flow_data(start_date, end_date)
#             if main_data is None or main_data.empty:
#                 raise Exception("无法获取主力资金数据")
            
#             self.update_status("正在合并和分析数据...")
            
#             # 合并数据
#             merged_data = self.merge_data(index_data, north_data, main_data, analyze_north)
#             if merged_data is None or merged_data.empty:
#                 raise Exception("合并数据失败")
            
#             # 保存当前数据
#             self.current_data = merged_data
            
#             # 计算相关系数
#             correlations = self.calculate_correlations(merged_data, analyze_north)
            
#             # 更新UI
#             self.root.after(0, lambda: self.update_results(merged_data, index_name, correlations, analyze_north))
            
#             self.update_status("分析完成")
#         except Exception as e:
#             # 显示错误信息
#             self.root.after(0, lambda: messagebox.showerror("分析错误", str(e)))
#             self.update_status("分析失败")
#         finally:
#             # 重新启用按钮
#             self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
    
#     def update_status(self, message):
#         """更新状态栏"""
#         self.status_var.set(message)
#         self.root.update_idletasks()
    
#     def get_market_index_data(self, index_code, start_date, end_date):
#         """获取指定指数的历史数据"""
#         try:
#             # 特殊处理科创50和沪深300指数
#             if index_code == "sh000688":  # 科创50
#                 df = ak.stock_zh_index_daily(symbol="sh000688")
#             elif index_code == "sh000300":  # 沪深300
#                 df = ak.stock_zh_index_daily(symbol="sh000300")
#             elif index_code == "sh000001":
#                 df = ak.stock_zh_index_daily(symbol="sh000001")
#             elif index_code == "sz399001":
#                 df = ak.stock_zh_index_daily(symbol="sz399001")
#             elif index_code == "sz399006":
#                 df = ak.stock_zh_index_daily(symbol="sz399006")
#             else:
#                 print(f"暂不支持该指数: {index_code}")
#                 return None
                
#             # 转换日期格式并筛选数据
#             df['date'] = pd.to_datetime(df['date'])
#             df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
#             # 计算涨跌幅(%)
#             df['pct_change'] = df['close'].pct_change() * 100
            
#             return df
#         except Exception as e:
#             print(f"获取指数数据时出错: {e}")
#             return None
    
#     def get_north_flow_data(self, start_date, end_date):
#         """获取北向资金净流入数据（兼容多种akshare版本）"""
#         try:
#             # 尝试最新接口
#             try:
#                 df = ak.stock_hsgt_north_net_flow_in_em()
#                 if df is None or df.empty:
#                     raise Exception("获取北向资金数据失败")
                    
#                 df['date'] = pd.to_datetime(df['date'])
#                 df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                 df = df.rename(columns={'net_amount': 'north_net_inflow'})
#                 # 转换为亿元单位
#                 df['north_net_inflow'] = df['north_net_inflow'] / 100000000
#                 return df[['date', 'north_net_inflow']]
#             except Exception as e1:
#                 print(f"尝试最新北向资金接口失败: {e1}")
                
#                 # 尝试旧接口
#                 try:
#                     df = ak.stock_individual_fund_flow_rank()
#                     if df is None or df.empty:
#                         raise Exception("获取北向资金数据失败")
                        
#                     df['date'] = pd.to_datetime(df['日期'])
#                     df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                     df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
#                     return df[['date', 'north_net_inflow']]
#                 except Exception as e2:
#                     print(f"尝试旧北向资金接口失败: {e2}")
                    
#                     # 尝试备选接口
#                     try:
#                         df = ak.stock_market_fund_flow()
#                         if df is None or df.empty:
#                             raise Exception("获取北向资金数据失败")
                            
#                         df['date'] = pd.to_datetime(df['日期'])
#                         df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                         df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
#                         return df[['date', 'north_net_inflow']]
#                     except Exception as e3:
#                         print(f"尝试备选北向资金接口失败: {e3}")
#                         raise Exception("无法获取北向资金数据，请确保akshare版本是最新的")
#         except Exception as e:
#             print(f"获取北向资金数据时出错: {e}")
#             return None
    
#     def get_main_money_flow_data(self, start_date, end_date):
#         """获取A股主力资金净流入数据（兼容多种akshare版本）"""
#         try:
#             # 尝试使用stock_market_fund_flow接口（新方法）
#             try:
#                 df = ak.stock_market_fund_flow()
#                 if df is None or df.empty:
#                     raise Exception("获取大盘资金流向数据失败")
                    
#                 df['date'] = pd.to_datetime(df['日期'])
#                 df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                 df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
                
#                 # 检查数据是否包含有效内容
#                 if 'main_net_inflow' in df.columns and not df['main_net_inflow'].isna().all():
#                     # 转换单位为亿元（根据数据实际情况判断是否需要转换）
#                     if df['main_net_inflow'].abs().max() > 10000:  # 如果数值超过1亿，认为是元单位
#                         df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                     return df[['date', 'main_net_inflow']]
#                 else:
#                     raise Exception("主力资金数据格式异常")
#             except Exception as e1:
#                 print(f"尝试大盘资金流向接口失败: {e1}")
                
#                 # 尝试使用北向资金数据作为主力资金的替代
#                 try:
#                     df = ak.stock_hsgt_north_net_flow_in_daily()
#                     if df is None or df.empty:
#                         raise Exception("获取北向资金数据失败")
                        
#                     df['date'] = pd.to_datetime(df['date'])
#                     df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
#                     df = df.rename(columns={'net_amount': 'main_net_inflow'})
#                     # 转换为亿元单位
#                     df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                     return df[['date', 'main_net_inflow']]
#                 except Exception as e2:
#                     print(f"尝试北向资金接口失败: {e2}")
                    
#                     # 尝试使用stock_individual_fund_flow接口
#                     try:
#                         df = ak.stock_individual_fund_flow(stock="all")
#                         if df is None or df.empty:
#                             raise Exception("获取个股资金流向数据失败")
                            
#                         # 检查是否包含必要的列
#                         if '日期' not in df.columns or '主力净流入-净额' not in df.columns:
#                             print(f"个股资金流向数据格式异常: {df.columns}")
#                             raise Exception("个股资金流向数据格式异常")
                            
#                         # 按日期分组并计算主力资金净流入总和
#                         df['date'] = pd.to_datetime(df['日期'])
#                         df = df.groupby('date')['主力净流入-净额'].sum().reset_index()
#                         df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
#                         # 筛选日期范围
#                         df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                        
#                         # 检查数据是否包含有效内容
#                         if 'main_net_inflow' in df.columns and not df['main_net_inflow'].isna().all():
#                             # 转换单位为亿元（根据数据实际情况判断是否需要转换）
#                             if df['main_net_inflow'].abs().max() > 10000:  # 如果数值超过1亿，认为是元单位
#                                 df['main_net_inflow'] = df['main_net_inflow'] / 100000000
#                             return df
#                         else:
#                             raise Exception("主力资金数据无有效内容")
#                     except Exception as e3:
#                         print(f"尝试个股资金流向接口失败: {e3}")
#                         raise Exception("无法获取主力资金数据，请确保akshare版本是最新的")
#         except Exception as e:
#             print(f"获取主力资金数据时出错: {e}")
#             return None
    
#     def merge_data(self, index_data, north_data, main_data, analyze_north):
#         """合并各类数据（支持北向资金开关）"""
#         try:
#             # 初始化合并数据
#             merged_data = pd.merge(main_data, index_data[['date', 'close', 'pct_change']], 
#                                   on='date', how='outer')
            
#             # 如果关注北向资金，添加北向数据
#             if analyze_north and north_data is not None and not north_data.empty:
#                 merged_data = pd.merge(merged_data, north_data[['date', 'north_net_inflow']], 
#                                       on='date', how='outer')
            
#             # 按日期排序并填充缺失值
#             merged_data = merged_data.sort_values('date')
#             merged_data = merged_data.ffill()  # 修复FutureWarning
            
#             return merged_data
#         except Exception as e:
#             print(f"合并数据时出错: {e}")
#             return None
    
#     def calculate_correlations(self, data, analyze_north):
#         """计算相关系数（根据北向开关过滤计算项）"""
#         if data is None or data.empty:
#             return None
        
#         correlations = {}
        
#         # 主力资金与指数涨跌幅的相关系数
#         if 'main_net_inflow' in data.columns and 'pct_change' in data.columns:
#             correlations['main'] = data['main_net_inflow'].corr(data['pct_change'])
        
#         # 北向资金相关系数仅在关注时计算
#         if analyze_north:
#             if 'north_net_inflow' in data.columns and 'pct_change' in data.columns:
#                 correlations['north'] = data['north_net_inflow'].corr(data['pct_change'])
            
#             if 'north_net_inflow' in data.columns and 'main_net_inflow' in data.columns:
#                 correlations['fund'] = data['north_net_inflow'].corr(data['main_net_inflow'])
        
#         return correlations
    
#     def update_results(self, data, index_name, correlations, analyze_north):
#         """更新结果显示（根据北向开关控制显示内容）"""
#         # 更新概览卡片
#         self.update_overview_cards(correlations, analyze_north)
        
#         # 绘制趋势图
#         self.draw_trend_chart(data, index_name, analyze_north)
        
#         # 绘制散点图
#         self.draw_scatter_chart(data, index_name, analyze_north)
        
#         # 更新数据表格
#         self.update_data_table(data, analyze_north)
        
#         # 更新统计信息
#         self.update_stats(data)
    
#     def update_overview_cards(self, correlations, analyze_north):
#         """根据北向开关更新概览卡片显示"""
#         # 主力资金相关性
#         self.main_value.set(f"{correlations.get('main', '--'):.2f}")
        
#         if analyze_north:
#             # 显示北向相关卡片
#             self.north_card.grid()
#             self.fund_card.grid()
#             self.main_card.grid_configure(column=1)
            
#             self.north_value.set(f"{correlations.get('north', '--'):.2f}")
#             self.fund_value.set(f"{correlations.get('fund', '--'):.2f}")
#         else:
#             # 隐藏北向相关卡片
#             self.north_card.grid_remove()
#             self.fund_card.grid_remove()
#             self.main_card.grid_configure(column=0, columnspan=3)
        
#         # 确保布局正确
#         self.overview_frame.update_idletasks()
    
#     def draw_trend_chart(self, data, index_name, analyze_north):
#         """绘制趋势图"""
#         self.trend_ax.clear()
#         dates = data['date'].dt.strftime('%Y-%m-%d')
        
#         # 绘制指数曲线
#         self.trend_ax.plot(dates, data['close'], 'b-', label='指数收盘价')
#         self.trend_ax.set_ylabel('指数收盘价', color='b')
#         self.trend_ax.tick_params(axis='y', labelcolor='b')
        
#         ax2 = self.trend_ax.twinx()
        
#         # 绘制主力资金柱状图（正数用红色，负数用绿色）
#         bar_width = 0.35
#         main_positive = data['main_net_inflow'].clip(lower=0)
#         main_negative = data['main_net_inflow'].clip(upper=0)
        
#         ax2.bar(dates, main_positive, width=bar_width, alpha=0.5, color='red', label='主力资金净流入')
#         ax2.bar(dates, main_negative, width=bar_width, alpha=0.5, color='green', label='主力资金净流出')
        
#         # 绘制北向资金柱状图（如果关注）
#         if analyze_north and 'north_net_inflow' in data.columns:
#             north_positive = data['north_net_inflow'].clip(lower=0)
#             north_negative = data['north_net_inflow'].clip(upper=0)
            
#             ax2.bar([x + bar_width for x in range(len(dates))], north_positive, 
#                    width=bar_width, alpha=0.5, color='purple', label='北向资金净流入')
#             ax2.bar([x + bar_width for x in range(len(dates))], north_negative, 
#                    width=bar_width, alpha=0.5, color='blue', label='北向资金净流出')
        
#         ax2.set_ylabel('资金净流入(亿)', color='k')
#         ax2.tick_params(axis='y', labelcolor='k')
        
#         # 生成图例
#         handles, labels = self.trend_ax.get_legend_handles_labels()
#         handles.append(plt.Rectangle((0,0),1,1,fc='red', alpha=0.5))
#         labels.append('主力资金净流入')
#         handles.append(plt.Rectangle((0,0),1,1,fc='green', alpha=0.5))
#         labels.append('主力资金净流出')
        
#         if analyze_north:
#             handles.append(plt.Rectangle((0,0),1,1,fc='purple', alpha=0.5))
#             labels.append('北向资金净流入')
#             handles.append(plt.Rectangle((0,0),1,1,fc='blue', alpha=0.5))
#             labels.append('北向资金净流出')
        
#         ax2.legend(handles, labels, loc='upper left')
        
#         self.trend_ax.set_title(f'{index_name}与资金流向趋势图')
#         self.trend_ax.set_xticks(range(len(dates)))
#         self.trend_ax.set_xticklabels(dates, rotation=45, ha='right')
#         self.trend_fig.tight_layout()
#         self.trend_canvas.draw()
    
#     def draw_scatter_chart(self, data, index_name, analyze_north):
#         """绘制散点图"""
#         self.scatter_ax.clear()
        
#         # 主力资金散点（正数用红色，负数用绿色）
#         main_positive = data[data['main_net_inflow'] >= 0]
#         main_negative = data[data['main_net_inflow'] < 0]
        
#         self.scatter_ax.scatter(main_positive['main_net_inflow'], main_positive['pct_change'], 
#                                c='red', alpha=0.5, label='主力资金净流入')
#         self.scatter_ax.scatter(main_negative['main_net_inflow'], main_negative['pct_change'], 
#                                c='green', alpha=0.5, label='主力资金净流出')
        
#         # 北向资金散点（如果关注）
#         if analyze_north and 'north_net_inflow' in data.columns:
#             north_positive = data[data['north_net_inflow'] >= 0]
#             north_negative = data[data['north_net_inflow'] < 0]
            
#             self.scatter_ax.scatter(north_positive['north_net_inflow'], north_positive['pct_change'], 
#                                    c='purple', alpha=0.5, label='北向资金净流入')
#             self.scatter_ax.scatter(north_negative['north_net_inflow'], north_negative['pct_change'], 
#                                    c='blue', alpha=0.5, label='北向资金净流出')
        
#         self.scatter_ax.set_xlabel('资金净流入(亿)')
#         self.scatter_ax.set_ylabel('涨跌幅(%)')
#         self.scatter_ax.set_title(f'资金净流入与{index_name}涨跌幅关系')
#         self.scatter_ax.legend()
#         self.scatter_fig.tight_layout()
#         self.scatter_canvas.draw()
    
#     def update_data_table(self, data, analyze_north):
#         """根据北向开关更新数据表格列，并为主力资金设置颜色"""
#         # 定义列
#         columns = ("日期", "指数收盘价", "涨跌幅(%)", "主力资金净流入(亿)")
#         if analyze_north and 'north_net_inflow' in data.columns:
#             columns += ("北向资金净流入(亿)",)
        
#         # 更新列配置
#         self.data_tree['columns'] = columns
#         for col in columns:
#             self.data_tree.heading(col, text=col)
#             self.data_tree.column(col, width=150, anchor=tk.CENTER)
        
#         # 清空数据
#         for item in self.data_tree.get_children():
#             self.data_tree.delete(item)
        
#         # 填充数据并设置主力资金的颜色
#         for i, row in data.iterrows():
#             values = [
#                 row['date'].strftime('%Y-%m-%d'),
#                 f"{row['close']:.2f}",
#                 f"{row['pct_change']:.2f}",
#                 f"{row['main_net_inflow']:.2f}"
#             ]
#             if analyze_north:
#                 values.append(f"{row.get('north_net_inflow', '--'):.2f}")
            
#             # 插入数据行
#             item = self.data_tree.insert("", "end", values=values)
            
#             # 设置主力资金列的颜色
#             main_inflow = row['main_net_inflow']
#             if main_inflow > 0:
#                 self.data_tree.set(item, "主力资金净流入(亿)", f"{main_inflow:.2f}")
#                 self.data_tree.item(item, tags=("positive",))
#             elif main_inflow < 0:
#                 self.data_tree.set(item, "主力资金净流入(亿)", f"{main_inflow:.2f}")
#                 self.data_tree.item(item, tags=("negative",))
        
#         # 配置标签样式
#         self.data_tree.tag_configure("positive", foreground="red")
#         self.data_tree.tag_configure("negative", foreground="green")
    
#     def update_stats(self, data):
#         """更新统计信息"""
#         if 'main_net_inflow' in data.columns:
#             # 计算统计数据
#             max_inflow = data['main_net_inflow'].max()
#             max_outflow = data['main_net_inflow'].min()
#             avg_inflow = data['main_net_inflow'].mean()
#             total_inflow = data['main_net_inflow'].sum()
            
#             # 更新标签
#             self.max_inflow.set(f"最大净流入: {max_inflow:.2f} 亿元")
#             self.max_outflow.set(f"最大净流出: {max_outflow:.2f} 亿元")
#             self.avg_inflow.set(f"平均净流入: {avg_inflow:.2f} 亿元")
#             self.total_inflow.set(f"总净流入: {total_inflow:.2f} 亿元")
            
#             # 为最大净流入和净流出设置颜色
#             if max_inflow > 0:
#                 self.max_inflow.set(f"最大净流入: {max_inflow:.2f} 亿元")
#                 self.max_inflow_label.configure(foreground="red")
#             else:
#                 self.max_inflow_label.configure(foreground="black")
            
#             if max_outflow < 0:
#                 self.max_outflow.set(f"最大净流出: {max_outflow:.2f} 亿元")
#                 self.max_outflow_label.configure(foreground="green")
#             else:
#                 self.max_outflow_label.configure(foreground="black")
#         else:
#             # 如果没有主力资金数据，显示默认信息
#             self.max_inflow.set("最大净流入: -- 亿元")
#             self.max_outflow.set("最大净流出: -- 亿元")
#             self.avg_inflow.set("平均净流入: -- 亿元")
#             self.total_inflow.set("总净流入: -- 亿元")
    
#     def export_data(self):
#         """导出数据到CSV文件"""
#         if self.current_data is None or self.current_data.empty:
#             messagebox.showinfo("导出数据", "没有数据可导出")
#             return
        
#         from tkinter import filedialog
        
#         # 获取保存路径
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".csv",
#             filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
#             title="保存数据"
#         )
        
#         if not file_path:
#             return
        
#         try:
#             # 保存数据
#             self.current_data.to_csv(file_path, index=False, encoding='utf-8-sig')
#             messagebox.showinfo("导出成功", f"数据已成功导出到 {file_path}")
#         except Exception as e:
#             messagebox.showerror("导出失败", f"导出数据时出错: {str(e)}")

# def main():
#     root = tk.Tk()
#     app = StockAnalysisApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()


import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading
import re
from tkcalendar import Calendar, DateEntry  # 导入日历组件

# 设置中文字体
matplotlib.use("TkAgg")
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

class DatePicker(ttk.Frame):
    """日期选择器组件"""
    def __init__(self, parent, default_date=None):
        super().__init__(parent)
        self.parent = parent
        
        # 如果没有提供默认日期，使用今天的日期
        if default_date:
            self.date_var = tk.StringVar(value=default_date.strftime('%Y-%m-%d'))
        else:
            self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        
        # 创建日期输入框
        self.date_entry = DateEntry(
            self, 
            textvariable=self.date_var, 
            width=12, 
            date_pattern='yyyy-mm-dd',
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # 创建日期选择按钮
        self.date_btn = ttk.Button(self, text="📅", command=self.select_date)
        self.date_btn.pack(side=tk.LEFT)
    
    def get_date(self):
        """获取选择的日期"""
        try:
            return datetime.strptime(self.date_var.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("日期格式错误", "请使用YYYY-MM-DD格式的日期")
            return None
    
    def select_date(self):
        """打开日期选择对话框"""
        def on_date_selected():
            selected_date = cal.selection_get()
            self.date_var.set(selected_date.strftime('%Y-%m-%d'))
            top.destroy()
        
        top = tk.Toplevel(self)
        top.title("选择日期")
        top.geometry("300x250")
        
        # 创建日历控件
        cal = Calendar(
            top,
            font="Arial 10",
            selectmode='day',
            cursor="hand1",
            year=self.get_date().year,
            month=self.get_date().month,
            day=self.get_date().day
        )
        cal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建确认按钮
        ttk.Button(top, text="确认", command=on_date_selected).pack(pady=10)

class StockAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A股资金流向与指数关系分析")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 数据缓存
        self.current_data = None
        
        # 北向资金开关
        self.north_enabled = tk.BooleanVar(value=False)
        
        # 创建界面
        self.create_widgets()
        
        # 检查akshare版本
        self.check_akshare_version()
        
    def check_akshare_version(self):
        """检查akshare版本并显示提示"""
        try:
            version = ak.__version__
            self.status_var.set(f"已加载 akshare v{version}")
            # 检查是否为较新版本
            major, minor, _ = map(int, re.findall(r'\d+', version)[:3])
            if major < 1 or (major == 1 and minor < 30):
                messagebox.showinfo("版本提示", 
                    f"您的akshare版本为{version}，建议升级到最新版本以获取最佳兼容性。\n"
                    "可通过命令: 'pip install akshare --upgrade' 进行升级。")
        except Exception as e:
            print(f"检查akshare版本时出错: {e}")
            self.status_var.set("无法确定akshare版本，请确保已安装最新版本")
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 控制面板
        control_frame = ttk.LabelFrame(main_frame, text="分析参数设置", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 指数选择
        ttk.Label(control_frame, text="选择指数:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.index_var = tk.StringVar(value="sh000001")
        index_frame = ttk.Frame(control_frame)
        index_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        index_options = [
            ("上证指数", "sh000001"),
            ("深证成指", "sz399001"),
            ("创业板指", "sz399006"),
            ("科创50", "sh000688"),
            ("沪深300", "sh000300")
        ]
        
        # 动态计算每行显示的指数选项数量
        options_per_row = 3
        for i, (text, value) in enumerate(index_options):
            row = i // options_per_row
            col = i % options_per_row
            ttk.Radiobutton(index_frame, text=text, variable=self.index_var, value=value).grid(row=row, column=col, padx=10, pady=5)
        
        # 日期选择
        ttk.Label(control_frame, text="开始日期:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.start_date_picker = DatePicker(control_frame, datetime.now() - timedelta(days=30))
        self.start_date_picker.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(control_frame, text="结束日期:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.end_date_picker = DatePicker(control_frame, datetime.now())
        self.end_date_picker.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # 资金类型选择
        ttk.Label(control_frame, text="关注资金:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        fund_frame = ttk.Frame(control_frame)
        fund_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.north_check = ttk.Checkbutton(fund_frame, text="北向资金", variable=self.north_enabled)
        self.north_check.grid(row=0, column=0, padx=5)
        self.main_check = ttk.Checkbutton(fund_frame, text="主力资金", variable=tk.BooleanVar(value=True))
        self.main_check.grid(row=0, column=1, padx=5)
        
        # 分析按钮
        self.analyze_btn = ttk.Button(control_frame, text="开始分析", command=self.start_analysis)
        self.analyze_btn.grid(row=0, column=2, rowspan=5, padx=20, pady=5, sticky=tk.EW)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 结果区域 - 使用Notebook创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # 概览选项卡
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text="分析概览")
        
        # 趋势图选项卡
        self.trend_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trend_frame, text="资金与指数趋势")
        
        # 散点图选项卡
        self.scatter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scatter_frame, text="相关性分析")
        
        # 数据表格选项卡
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="详细数据")
        
        # 统计信息选项卡
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="统计信息")
        
        # 创建趋势图
        self.trend_fig = Figure(figsize=(10, 5), dpi=100)
        self.trend_ax = self.trend_fig.add_subplot(111)
        self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, master=self.trend_frame)
        self.trend_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 创建散点图
        self.scatter_fig = Figure(figsize=(10, 5), dpi=100)
        self.scatter_ax = self.scatter_fig.add_subplot(111)
        self.scatter_canvas = FigureCanvasTkAgg(self.scatter_fig, master=self.scatter_frame)
        self.scatter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 创建数据表格
        self.data_tree = ttk.Treeview(self.data_frame)
        scrollbar = ttk.Scrollbar(self.data_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        self.data_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.data_tree.pack(fill=tk.BOTH, expand=True)
        
        # 导出按钮
        self.export_btn = ttk.Button(self.data_frame, text="导出数据", command=self.export_data)
        self.export_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # 创建概览卡片
        self.create_overview_cards()
        
        # 创建统计信息卡片
        self.create_stats_cards()
    
    def create_overview_cards(self):
        # 初始卡片布局
        self.north_card = ttk.LabelFrame(self.overview_frame, text="北向资金相关性", padding="10")
        self.north_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        self.north_card.grid_remove()
        
        self.main_card = ttk.LabelFrame(self.overview_frame, text="主力资金相关性", padding="10")
        self.main_card.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        
        self.fund_card = ttk.LabelFrame(self.overview_frame, text="资金协同性", padding="10")
        self.fund_card.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)
        self.fund_card.grid_remove()
        
        self.north_value = tk.StringVar(value="--")
        ttk.Label(self.north_card, textvariable=self.north_value, font=("SimHei", 24, "bold")).pack(pady=10)
        ttk.Label(self.north_card, text="北向资金净流入与指数涨跌幅的相关系数").pack()
        
        self.main_value = tk.StringVar(value="--")
        ttk.Label(self.main_card, textvariable=self.main_value, font=("SimHei", 24, "bold")).pack(pady=10)
        ttk.Label(self.main_card, text="主力资金净流入与指数涨跌幅的相关系数").pack()
        
        self.fund_value = tk.StringVar(value="--")
        ttk.Label(self.fund_card, textvariable=self.fund_value, font=("SimHei", 24, "bold")).pack(pady=10)
        ttk.Label(self.fund_card, text="北向资金与主力资金的协同系数").pack()
        
        # 设置列权重
        self.overview_frame.grid_columnconfigure(0, weight=1)
        self.overview_frame.grid_columnconfigure(1, weight=1)
        self.overview_frame.grid_columnconfigure(2, weight=1)
    
    def create_stats_cards(self):
        # 主力资金统计卡片
        self.main_stats_card = ttk.LabelFrame(self.stats_frame, text="主力资金统计", padding="10")
        self.main_stats_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建统计信息标签
        self.max_inflow = tk.StringVar(value="最大净流入: -- 亿元")
        self.max_outflow = tk.StringVar(value="最大净流出: -- 亿元")
        self.avg_inflow = tk.StringVar(value="平均净流入: -- 亿元")
        self.total_inflow = tk.StringVar(value="总净流入: -- 亿元")
        
        self.max_inflow_label = ttk.Label(self.main_stats_card, textvariable=self.max_inflow, font=("SimHei", 14))
        self.max_inflow_label.pack(anchor=tk.W, pady=5)
        self.max_outflow_label = ttk.Label(self.main_stats_card, textvariable=self.max_outflow, font=("SimHei", 14))
        self.max_outflow_label.pack(anchor=tk.W, pady=5)
        self.avg_inflow_label = ttk.Label(self.main_stats_card, textvariable=self.avg_inflow, font=("SimHei", 14))
        self.avg_inflow_label.pack(anchor=tk.W, pady=5)
        self.total_inflow_label = ttk.Label(self.main_stats_card, textvariable=self.total_inflow, font=("SimHei", 14))
        self.total_inflow_label.pack(anchor=tk.W, pady=5)
    
    def start_analysis(self):
        """开始分析"""
        # 禁用按钮
        self.analyze_btn.config(state=tk.DISABLED)
        self.status_var.set("正在获取数据...")
        
        # 获取日期
        start_date = self.start_date_picker.get_date()
        end_date = self.end_date_picker.get_date()
        
        # 验证日期
        if not start_date or not end_date:
            self.status_var.set("日期格式错误")
            self.analyze_btn.config(state=tk.NORMAL)
            return
        
        if start_date >= end_date:
            messagebox.showerror("日期错误", "开始日期必须早于结束日期")
            self.status_var.set("就绪")
            self.analyze_btn.config(state=tk.NORMAL)
            return
        
        # 在单独的线程中执行分析，避免阻塞UI
        analysis_thread = threading.Thread(target=self.perform_analysis, args=(start_date, end_date))
        analysis_thread.daemon = True
        analysis_thread.start()
    
    def perform_analysis(self, start_date, end_date):
        try:
            # 获取参数
            index_code = self.index_var.get()
            analyze_north = self.north_enabled.get()
            analyze_main = True
            
            # 获取指数名称
            index_names = {
                "sh000001": "上证指数",
                "sz399001": "深证成指",
                "sz399006": "创业板指",
                "sh000688": "科创50",
                "sh000300": "沪深300"
            }
            index_name = index_names.get(index_code, "未知指数")
            
            # 更新状态
            self.update_status(f"正在获取{index_name}数据...")
            
            # 获取数据
            index_data = self.get_market_index_data(index_code, start_date, end_date)
            if index_data is None or index_data.empty:
                raise Exception(f"无法获取{index_name}数据")
            
            north_data = None
            if analyze_north:
                self.update_status("正在获取北向资金数据...")
                north_data = self.get_north_flow_data(start_date, end_date)
                if north_data is None or north_data.empty:
                    raise Exception("无法获取北向资金数据")
            
            self.update_status("正在获取主力资金数据...")
            main_data = self.get_main_money_flow_data(start_date, end_date)
            if main_data is None or main_data.empty:
                raise Exception("无法获取主力资金数据")
            
            self.update_status("正在合并和分析数据...")
            
            # 合并数据
            merged_data = self.merge_data(index_data, north_data, main_data, analyze_north)
            if merged_data is None or merged_data.empty:
                raise Exception("合并数据失败")
            
            # 保存当前数据
            self.current_data = merged_data
            
            # 计算相关系数
            correlations = self.calculate_correlations(merged_data, analyze_north)
            
            # 更新UI
            self.root.after(0, lambda: self.update_results(merged_data, index_name, correlations, analyze_north))
            
            self.update_status("分析完成")
        except Exception as e:
            # 显示错误信息
            self.root.after(0, lambda: messagebox.showerror("分析错误", str(e)))
            self.update_status("分析失败")
        finally:
            # 重新启用按钮
            self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def get_market_index_data(self, index_code, start_date, end_date):
        """获取指定指数的历史数据"""
        try:
            # 特殊处理科创50和沪深300指数
            if index_code == "sh000688":  # 科创50
                df = ak.stock_zh_index_daily(symbol="sh000688")
            elif index_code == "sh000300":  # 沪深300
                df = ak.stock_zh_index_daily(symbol="sh000300")
            elif index_code == "sh000001":
                df = ak.stock_zh_index_daily(symbol="sh000001")
            elif index_code == "sz399001":
                df = ak.stock_zh_index_daily(symbol="sz399001")
            elif index_code == "sz399006":
                df = ak.stock_zh_index_daily(symbol="sz399006")
            else:
                print(f"暂不支持该指数: {index_code}")
                return None
                
            # 转换日期格式并筛选数据
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
            # 计算涨跌幅(%)
            df['pct_change'] = df['close'].pct_change() * 100
            
            return df
        except Exception as e:
            print(f"获取指数数据时出错: {e}")
            return None
    
    def get_north_flow_data(self, start_date, end_date):
        """获取北向资金净流入数据（兼容多种akshare版本）"""
        try:
            # 尝试最新接口
            try:
                df = ak.stock_hsgt_north_net_flow_in_em()
                if df is None or df.empty:
                    raise Exception("获取北向资金数据失败")
                    
                df['date'] = pd.to_datetime(df['date'])
                df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                df = df.rename(columns={'net_amount': 'north_net_inflow'})
                # 转换为亿元单位
                df['north_net_inflow'] = df['north_net_inflow'] / 100000000
                return df[['date', 'north_net_inflow']]
            except Exception as e1:
                print(f"尝试最新北向资金接口失败: {e1}")
                
                # 尝试旧接口
                try:
                    df = ak.stock_individual_fund_flow_rank()
                    if df is None or df.empty:
                        raise Exception("获取北向资金数据失败")
                        
                    df['date'] = pd.to_datetime(df['日期'])
                    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                    df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
                    return df[['date', 'north_net_inflow']]
                except Exception as e2:
                    print(f"尝试旧北向资金接口失败: {e2}")
                    
                    # 尝试备选接口
                    try:
                        df = ak.stock_market_fund_flow()
                        if df is None or df.empty:
                            raise Exception("获取北向资金数据失败")
                            
                        df['date'] = pd.to_datetime(df['日期'])
                        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                        df = df.rename(columns={'主力净流入-净额': 'north_net_inflow'})
                        return df[['date', 'north_net_inflow']]
                    except Exception as e3:
                        print(f"尝试备选北向资金接口失败: {e3}")
                        raise Exception("无法获取北向资金数据，请确保akshare版本是最新的")
        except Exception as e:
            print(f"获取北向资金数据时出错: {e}")
            return None
    
    def get_main_money_flow_data(self, start_date, end_date):
        """获取A股主力资金净流入数据（兼容多种akshare版本）"""
        try:
            # 尝试使用stock_market_fund_flow接口（新方法）
            try:
                df = ak.stock_market_fund_flow()
                if df is None or df.empty:
                    raise Exception("获取大盘资金流向数据失败")
                    
                df['date'] = pd.to_datetime(df['日期'])
                df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
                
                # 检查数据是否包含有效内容
                if 'main_net_inflow' in df.columns and not df['main_net_inflow'].isna().all():
                    # 转换单位为亿元（根据数据实际情况判断是否需要转换）
                    if df['main_net_inflow'].abs().max() > 10000:  # 如果数值超过1亿，认为是元单位
                        df['main_net_inflow'] = df['main_net_inflow'] / 100000000
                    return df[['date', 'main_net_inflow']]
                else:
                    raise Exception("主力资金数据格式异常")
            except Exception as e1:
                print(f"尝试大盘资金流向接口失败: {e1}")
                
                # 尝试使用北向资金数据作为主力资金的替代
                try:
                    df = ak.stock_hsgt_north_net_flow_in_daily()
                    if df is None or df.empty:
                        raise Exception("获取北向资金数据失败")
                        
                    df['date'] = pd.to_datetime(df['date'])
                    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                    df = df.rename(columns={'net_amount': 'main_net_inflow'})
                    # 转换为亿元单位
                    df['main_net_inflow'] = df['main_net_inflow'] / 100000000
                    return df[['date', 'main_net_inflow']]
                except Exception as e2:
                    print(f"尝试北向资金接口失败: {e2}")
                    
                    # 尝试使用stock_individual_fund_flow接口
                    try:
                        df = ak.stock_individual_fund_flow(stock="all")
                        if df is None or df.empty:
                            raise Exception("获取个股资金流向数据失败")
                            
                        # 检查是否包含必要的列
                        if '日期' not in df.columns or '主力净流入-净额' not in df.columns:
                            print(f"个股资金流向数据格式异常: {df.columns}")
                            raise Exception("个股资金流向数据格式异常")
                            
                        # 按日期分组并计算主力资金净流入总和
                        df['date'] = pd.to_datetime(df['日期'])
                        df = df.groupby('date')['主力净流入-净额'].sum().reset_index()
                        df = df.rename(columns={'主力净流入-净额': 'main_net_inflow'})
                        # 筛选日期范围
                        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                        
                        # 检查数据是否包含有效内容
                        if 'main_net_inflow' in df.columns and not df['main_net_inflow'].isna().all():
                            # 转换单位为亿元（根据数据实际情况判断是否需要转换）
                            if df['main_net_inflow'].abs().max() > 10000:  # 如果数值超过1亿，认为是元单位
                                df['main_net_inflow'] = df['main_net_inflow'] / 100000000
                            return df
                        else:
                            raise Exception("主力资金数据无有效内容")
                    except Exception as e3:
                        print(f"尝试个股资金流向接口失败: {e3}")
                        raise Exception("无法获取主力资金数据，请确保akshare版本是最新的")
        except Exception as e:
            print(f"获取主力资金数据时出错: {e}")
            return None
    
    def merge_data(self, index_data, north_data, main_data, analyze_north):
        """合并各类数据（支持北向资金开关）"""
        try:
            # 初始化合并数据
            merged_data = pd.merge(main_data, index_data[['date', 'close', 'pct_change']], 
                                  on='date', how='outer')
            
            # 如果关注北向资金，添加北向数据
            if analyze_north and north_data is not None and not north_data.empty:
                merged_data = pd.merge(merged_data, north_data[['date', 'north_net_inflow']], 
                                      on='date', how='outer')
            
            # 按日期排序并填充缺失值
            merged_data = merged_data.sort_values('date')
            merged_data = merged_data.ffill()  # 修复FutureWarning
            
            return merged_data
        except Exception as e:
            print(f"合并数据时出错: {e}")
            return None
    
    def calculate_correlations(self, data, analyze_north):
        """计算相关系数（根据北向开关过滤计算项）"""
        if data is None or data.empty:
            return None
        
        correlations = {}
        
        # 主力资金与指数涨跌幅的相关系数
        if 'main_net_inflow' in data.columns and 'pct_change' in data.columns:
            correlations['main'] = data['main_net_inflow'].corr(data['pct_change'])
        
        # 北向资金相关系数仅在关注时计算
        if analyze_north:
            if 'north_net_inflow' in data.columns and 'pct_change' in data.columns:
                correlations['north'] = data['north_net_inflow'].corr(data['pct_change'])
            
            if 'north_net_inflow' in data.columns and 'main_net_inflow' in data.columns:
                correlations['fund'] = data['north_net_inflow'].corr(data['main_net_inflow'])
        
        return correlations
    
    def update_results(self, data, index_name, correlations, analyze_north):
        """更新结果显示（根据北向开关控制显示内容）"""
        # 更新概览卡片
        self.update_overview_cards(correlations, analyze_north)
        
        # 绘制趋势图
        self.draw_trend_chart(data, index_name, analyze_north)
        
        # 绘制散点图
        self.draw_scatter_chart(data, index_name, analyze_north)
        
        # 更新数据表格
        self.update_data_table(data, analyze_north)
        
        # 更新统计信息
        self.update_stats(data)
    
    def update_overview_cards(self, correlations, analyze_north):
        """根据北向开关更新概览卡片显示"""
        # 主力资金相关性
        self.main_value.set(f"{correlations.get('main', '--'):.2f}")
        
        if analyze_north:
            # 显示北向相关卡片
            self.north_card.grid()
            self.fund_card.grid()
            self.main_card.grid_configure(column=1)
            
            self.north_value.set(f"{correlations.get('north', '--'):.2f}")
            self.fund_value.set(f"{correlations.get('fund', '--'):.2f}")
        else:
            # 隐藏北向相关卡片
            self.north_card.grid_remove()
            self.fund_card.grid_remove()
            self.main_card.grid_configure(column=0, columnspan=3)
        
        # 确保布局正确
        self.overview_frame.update_idletasks()
    
    def draw_trend_chart(self, data, index_name, analyze_north):
        """绘制趋势图"""
        # 彻底清除画布和坐标轴
        self.trend_fig.clear()
        self.trend_ax = self.trend_fig.add_subplot(111)
        
        dates = data['date'].dt.strftime('%Y-%m-%d')
        
        # 绘制指数曲线
        self.trend_ax.plot(dates, data['close'], 'b-', label='指数收盘价')
        self.trend_ax.set_ylabel('指数收盘价', color='b')
        self.trend_ax.tick_params(axis='y', labelcolor='b')
        
        ax2 = self.trend_ax.twinx()
        
        # 绘制主力资金柱状图（正数用红色，负数用绿色）
        bar_width = 0.35
        main_positive = data['main_net_inflow'].clip(lower=0)
        main_negative = data['main_net_inflow'].clip(upper=0)
        
        ax2.bar(dates, main_positive, width=bar_width, alpha=0.5, color='red', label='主力资金净流入')
        ax2.bar(dates, main_negative, width=bar_width, alpha=0.5, color='green', label='主力资金净流出')
        
        # 绘制北向资金柱状图（如果关注）
        if analyze_north and 'north_net_inflow' in data.columns:
            north_positive = data['north_net_inflow'].clip(lower=0)
            north_negative = data['north_net_inflow'].clip(upper=0)
            
            ax2.bar([x + bar_width for x in range(len(dates))], north_positive, 
                   width=bar_width, alpha=0.5, color='purple', label='北向资金净流入')
            ax2.bar([x + bar_width for x in range(len(dates))], north_negative, 
                   width=bar_width, alpha=0.5, color='blue', label='北向资金净流出')
        
        ax2.set_ylabel('资金净流入(亿)', color='k')
        ax2.tick_params(axis='y', labelcolor='k')
        
        # 生成图例
        handles, labels = self.trend_ax.get_legend_handles_labels()
        handles.append(plt.Rectangle((0,0),1,1,fc='red', alpha=0.5))
        labels.append('主力资金净流入')
        handles.append(plt.Rectangle((0,0),1,1,fc='green', alpha=0.5))
        labels.append('主力资金净流出')
        
        if analyze_north:
            handles.append(plt.Rectangle((0,0),1,1,fc='purple', alpha=0.5))
            labels.append('北向资金净流入')
            handles.append(plt.Rectangle((0,0),1,1,fc='blue', alpha=0.5))
            labels.append('北向资金净流出')
        
        ax2.legend(handles, labels, loc='upper left')
        
        self.trend_ax.set_title(f'{index_name}与资金流向趋势图')
        self.trend_ax.set_xticks(range(len(dates)))
        self.trend_ax.set_xticklabels(dates, rotation=45, ha='right')
        self.trend_fig.tight_layout()
        self.trend_canvas.draw()
    
    def draw_scatter_chart(self, data, index_name, analyze_north):
        """绘制散点图"""
        # 彻底清除画布和坐标轴
        self.scatter_fig.clear()
        self.scatter_ax = self.scatter_fig.add_subplot(111)
        
        # 主力资金散点（正数用红色，负数用绿色）
        main_positive = data[data['main_net_inflow'] >= 0]
        main_negative = data[data['main_net_inflow'] < 0]
        
        self.scatter_ax.scatter(main_positive['main_net_inflow'], main_positive['pct_change'], 
                               c='red', alpha=0.5, label='主力资金净流入')
        self.scatter_ax.scatter(main_negative['main_net_inflow'], main_negative['pct_change'], 
                               c='green', alpha=0.5, label='主力资金净流出')
        
        # 北向资金散点（如果关注）
        if analyze_north and 'north_net_inflow' in data.columns:
            north_positive = data[data['north_net_inflow'] >= 0]
            north_negative = data[data['north_net_inflow'] < 0]
            
            self.scatter_ax.scatter(north_positive['north_net_inflow'], north_positive['pct_change'], 
                                   c='purple', alpha=0.5, label='北向资金净流入')
            self.scatter_ax.scatter(north_negative['north_net_inflow'], north_negative['pct_change'], 
                                   c='blue', alpha=0.5, label='北向资金净流出')
        
        self.scatter_ax.set_xlabel('资金净流入(亿)')
        self.scatter_ax.set_ylabel('涨跌幅(%)')
        self.scatter_ax.set_title(f'资金净流入与{index_name}涨跌幅关系')
        self.scatter_ax.legend()
        self.scatter_fig.tight_layout()
        self.scatter_canvas.draw()
    
    def update_data_table(self, data, analyze_north):
        """根据北向开关更新数据表格列，并为主力资金设置颜色"""
        # 定义列
        columns = ("日期", "指数收盘价", "涨跌幅(%)", "主力资金净流入(亿)")
        if analyze_north and 'north_net_inflow' in data.columns:
            columns += ("北向资金净流入(亿)",)
        
        # 更新列配置
        self.data_tree['columns'] = columns
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=150, anchor=tk.CENTER)
        
        # 清空数据
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # 填充数据并设置主力资金的颜色
        for i, row in data.iterrows():
            values = [
                row['date'].strftime('%Y-%m-%d'),
                f"{row['close']:.2f}",
                f"{row['pct_change']:.2f}",
                f"{row['main_net_inflow']:.2f}"
            ]
            if analyze_north:
                values.append(f"{row.get('north_net_inflow', '--'):.2f}")
            
            # 插入数据行
            item = self.data_tree.insert("", "end", values=values)
            
            # 设置主力资金列的颜色
            main_inflow = row['main_net_inflow']
            if main_inflow > 0:
                self.data_tree.set(item, "主力资金净流入(亿)", f"{main_inflow:.2f}")
                self.data_tree.item(item, tags=("positive",))
            elif main_inflow < 0:
                self.data_tree.set(item, "主力资金净流入(亿)", f"{main_inflow:.2f}")
                self.data_tree.item(item, tags=("negative",))
        
        # 配置标签样式
        self.data_tree.tag_configure("positive", foreground="red")
        self.data_tree.tag_configure("negative", foreground="green")
    
    def update_stats(self, data):
        """更新统计信息"""
        if 'main_net_inflow' in data.columns:
            # 计算统计数据
            max_inflow = data['main_net_inflow'].max()
            max_outflow = data['main_net_inflow'].min()
            avg_inflow = data['main_net_inflow'].mean()
            total_inflow = data['main_net_inflow'].sum()
            
            # 更新标签
            self.max_inflow.set(f"最大净流入: {max_inflow:.2f} 亿元")
            self.max_outflow.set(f"最大净流出: {max_outflow:.2f} 亿元")
            self.avg_inflow.set(f"平均净流入: {avg_inflow:.2f} 亿元")
            self.total_inflow.set(f"总净流入: {total_inflow:.2f} 亿元")
            
            # 为最大净流入和净流出设置颜色
            if max_inflow > 0:
                self.max_inflow.set(f"最大净流入: {max_inflow:.2f} 亿元")
                self.max_inflow_label.configure(foreground="red")
            else:
                self.max_inflow_label.configure(foreground="black")
            
            if max_outflow < 0:
                self.max_outflow.set(f"最大净流出: {max_outflow:.2f} 亿元")
                self.max_outflow_label.configure(foreground="green")
            else:
                self.max_outflow_label.configure(foreground="black")
        else:
            # 如果没有主力资金数据，显示默认信息
            self.max_inflow.set("最大净流入: -- 亿元")
            self.max_outflow.set("最大净流出: -- 亿元")
            self.avg_inflow.set("平均净流入: -- 亿元")
            self.total_inflow.set("总净流入: -- 亿元")
    
    def export_data(self):
        """导出数据到CSV文件"""
        if self.current_data is None or self.current_data.empty:
            messagebox.showinfo("导出数据", "没有数据可导出")
            return
        
        from tkinter import filedialog
        
        # 获取保存路径
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
            title="保存数据"
        )
        
        if not file_path:
            return
        
        try:
            # 保存数据
            self.current_data.to_csv(file_path, index=False, encoding='utf-8-sig')
            messagebox.showinfo("导出成功", f"数据已成功导出到 {file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出数据时出错: {str(e)}")

def main():
    root = tk.Tk()
    app = StockAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

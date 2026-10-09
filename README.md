# hiragana-chart.com

单页。主词 hiragana chart。46 个平假名、笔顺动画、点击读真人发音（预录 MP3）。没有片假名。

## 文件

- `index.html` / `styles.css` / `app.js` — 页面
- `audio/*.mp3` — 46 个假名真人发音（日语母语者音色预录，懒加载，点击才请求）
- `og-image.png` — 社交分享图 1200x630
- `llms.txt` — 给 AI 爬虫的完整图表数据（AEO）
- `robots.txt` / `sitemap.xml`

## 交互

- 点击格子：显示大字 + 罗马音 + 笔顺动画（按笔画顺序描画，编号标在起笔处）+ 播放发音
- Play audio：重播当前假名发音；Replay strokes：重播笔顺动画
- 深链：`hiragana-chart.com/#shi` 打开直接选中 し
- 页面加载不自动发音（之前版本有个 bug：加载即朗读，已修）

## 部署

1. 把这个目录推到 GitHub，仓库名可用 hiragana-chart.com。
2. Vercel：Add New → Project → Import 这个仓库 → Deploy。没有环境变量。
3. Cloudflare 添加站点 hiragana-chart.com，免费套餐。把 Cloudflare 给的 2 个 NS 填到 Namecheap。
4. Namecheap：Domain List → Manage → Nameservers → Custom DNS。
5. Vercel 添加域名 hiragana-chart.com。Cloudflare SSL/TLS 选 Full (Strict)。
6. 主域名用不带 www 的。www 做 301。http 跳 https。
7. 打开 https://hiragana-chart.com/ 确认页面后，再提交 Google Search Console 和 sitemap。
8. 发音 MP3 走 Vercel 静态托管即可（共 356KB，懒加载，不影响首屏）。

## 改动记录（2026-10-09 v2）

- 发音从 speechSynthesis 改为预录 MP3：各设备系统日语语音缺失/发音不准的问题彻底解决
- 笔顺图加逐笔描画动画 + 编号移到起笔处 + Replay strokes 按钮
- 修 bug：页面加载不再自动朗读
- SEO/AEO：标题收紧、加 favicon/theme-color/og:image、发音指南区块、FAQ 3→10 条并同步 FAQPage schema、llms.txt 扩充完整数据、#hash 深链

# CLAUDE.md — Energy & Logistics Dashboard
> קרא קובץ זה לפני כל שינוי בפרויקט.

---

## סקירת הפרויקט

דשבורד Streamlit בעברית RTL למנהלי רכש ולוגיסטיקה בחברת מזון/ייבוא.  
מציג מחירי נפט ושערי מטבע בזמן אמת, עם מחשבונים מהירים וייצוא לאקסל.

**GitHub:** `https://github.com/marom9/neft`  
**קהל יעד:** מנכ"ל, מנהלי רכש, מנהלי מכירות, מנהל ייבוא  
**Branding:** Developed by Marom Cohen | Marom-Media

---

## מבנה הפרויקט

```
C:\neft\
├── app.py            ← כל הקוד (קובץ יחיד, ~950 שורות)
├── requirements.txt  ← תלויות Python
├── run.bat           ← הפעלה מקומית בלחיצה אחת (Windows)
├── CLAUDE.md         ← המסמך הזה
└── .gitignore
```

**אין תיקיות נוספות.** הפרויקט מכוון להיות קובץ יחיד פשוט.

---

## ארכיטקטורת app.py (לפי סדר הקוד)

| שורות (בערך) | חלק |
|---|---|
| 1–8 | Imports |
| 10–18 | Page config |
| 20–328 | CSS ראשי — RTL, white-label, עיצוב Option A |
| 330–434 | CSS רספונסיבי — media queries tablet/mobile |
| 436–444 | ASSETS dict (4 נכסים) |
| 446–500 | Data layer: `fetch_series`, `safe_val`, `pct_diff` |
| 502–526 | `sparkline_svg` — SVG inline, width=100% |
| 528–580 | HTML helpers: `kpi_html`, `ch_cell`, `comparison_table_html` |
| 582–660 | `trend_chart` — Plotly |
| 662–685 | `build_excel` |
| 687–700 | Load data |
| 702–720 | Header |
| 722–746 | Settings expander |
| 748–775 | Alert banners (`_alert` helper) |
| 777–795 | KPI cards |
| 797–836 | Trend charts (2 שורות: נפט / מטבעות) |
| 838–845 | Comparison table |
| 847–930 | Calculators: המרת מטבע + עלות הובלה |
| 932–950 | Export to Excel |
| 952–960 | Footer |

---

## נכסים במעקב

```python
ASSETS = {
    "🛢️ נפט ברנט":  ("BZ=F",     "$/חבית", "#c0392b"),
    "🛢️ נפט WTI":   ("CL=F",     "$/חבית", "#e67e22"),
    "💵 דולר/שקל":  ("USDILS=X", "₪",      "#1d4ed8"),
    "💶 אירו/שקל":  ("EURILS=X", "₪",      "#6d28d9"),
}
```

להוספת נכס (למשל ליש"ט): הוסף שורה ל-`ASSETS`. הכל אחר מתעדכן אוטומטית.

---

## החלטות עיצוב מרכזיות

| נושא | החלטה | סיבה |
|---|---|---|
| עיצוב כללי | Option A — Clean Corporate | ניגודיות גבוהה, מתאים למשרד בהיר |
| פלטת צבעים | Navy `#0d1b2a`, אדום `#dc2626`, ירוק `#16a34a` | קריאות גבוהה |
| גופן | Heebo (Google Fonts) | RTL עברית, משקלים 300–900 |
| Layout | Sidebar הוסר, הגדרות ב-`st.expander` | RTL-friendly, נקי |
| ספארקליין | SVG inline, `width=100% + viewBox` | מתאים לכל רוחב כרטיס |
| Footer | HTML מותאם אישית | Streamlit footer מוסתר (white-label) |

---

## ❌ שגיאות שכבר עשינו — אל תחזור עליהן

### 1. `session=requests.Session()` ב-yfinance
```python
# ❌ שובר את ה-auth הפנימי של yfinance — כל הנתונים חוזרים ריקים
yf.download(ticker, session=my_session)

# ✅ תן ל-yfinance לנהל את הסשן שלו
yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
```

### 2. f-strings בתוך tuple-list לאזהרות מחיר
```python
# ❌ Python מחשב את כל ה-f-strings לפני בדיקת התנאי
# אם brent_cur=None → TypeError: unsupported format
for triggered, msg in [
    (brent_cur and brent_cur > threshold,
     f"${brent_cur:.2f}"),   # ← קורס כאן אם brent_cur=None
]:

# ✅ if נפרד לכל התראה
if brent_cur is not None and brent_cur > threshold:
    show_alert(f"${brent_cur:.2f}")
```

### 3. build_excel ללא fallback sheet
```python
# ❌ openpyxl זורק IndexError אם לא נכתב אף גיליון
with pd.ExcelWriter(buf) as writer:
    for ...:
        if len(s) == 0: continue   # אם כולם ריקים → קריסה

# ✅ תמיד צור לפחות גיליון אחד
if not wrote_any:
    fallback_df.to_excel(writer, sheet_name="Note")
```

### 4. עברית ב-run.bat
```bat
:: ❌ CMD מנסה לפרש שורות עברית כפקודות
echo מתקין תלויות...

:: ✅ אנגלית בלבד ב-.bat
echo Installing dependencies...
```

### 5. `streamlit run` ישיר (Windows PATH)
```bat
:: ❌ 'streamlit' is not recognized...
streamlit run app.py

:: ✅
python -m streamlit run app.py
```

### 6. עברית ב-`st.markdown` כ-key ב-Edit tool
ה-Edit tool מתקשה לזהות Hebrew strings בקובץ בגלל encoding.  
פתרון: השתמש ב-Python script דרך Bash לביצוע החלפה:
```python
with open('app.py', encoding='utf-8') as f: src = f.read()
src = src.replace(old, new)
with open('app.py', 'w', encoding='utf-8') as f: f.write(src)
```

---

## CSS — נקודות חשובות

### הסתרת Streamlit Chrome
```css
#MainMenu, header[data-testid="stHeader"], footer,
div[data-testid="stToolbar"], .stDeployButton { display: none !important; }
```

### RTL — selectors קריטיים
```css
div[data-testid="stHorizontalBlock"],
div[data-testid="stVerticalBlock"],
div[data-testid="column"] { direction: rtl !important; }
```

### Mobile stacking
```css
@media (max-width: 900px) {
    div[data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    div[data-testid="column"] { width: 100% !important; min-width: 100% !important; }
}
```

---

## Git — מצב נוכחי

```
branch: main
remote: https://github.com/marom9/neft.git

commits (עדכני ביותר ראשון):
006feb0  Improve mobile layout: full-width sparklines, KPI value+badge inline
a06e38a  Revert custom requests session — let yfinance manage its own auth
f6a1172  Fix IndexError in build_excel when all data fetches fail
b94cf14  Fix yfinance fetch failures on Streamlit Cloud
2c65a7f  Fix TypeError in price alert banners on failed data fetch
7df311c  Initial Release - Energy & Logistics Dashboard
```

---

## רשימת שיפורים אפשריים עתידיים

- [ ] הוספת ליש"ט/שקל חזרה (הוסר לפי בקשה)
- [ ] מקור נתונים חלופי (Alpha Vantage) אם Yahoo Finance ימשיך לחסום Cloud IPs
- [ ] שמירת ספי ההתראות ב-`st.session_state` כדי לשמור בין רענונים
- [ ] גיליון "סיכום" בקובץ האקסל עם השוואה היסטורית
- [ ] Dark mode toggle (Option B מהמוקאפים)

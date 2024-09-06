
## 🏋 Leaffit

> Generate Wendler Exercise Sheets based on your One Rep Max weights  
> 
> Visit the live site here https://kyeongsupchoi.pythonanywhere.com
> 
> Wendler Program explanation at https://www.t-nation.com/workouts/5-3-1-how-to-build-pure-strength/

## 📂 Code-base structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                               # Implements app configuration
   |    |-- settings.py                    # Defines Global Settings
   |    |-- wsgi.py                        # Start the app in production
   |    |-- urls.py                        # Define URLs served by all apps/nodes
   |
   |-- apps/
   |    |
   |    |-- home/                          # A simple app that serve HTML files
   |    |    |-- views.py                  # Serve HTML pages for authenticated users
   |    |    |-- urls.py                   # Define some super simple routes  
   |    |
   |    |-- authentication/                # Handles auth routes (login and register)
   |    |    |-- urls.py                   # Define authentication routes  
   |    |    |-- views.py                  # Handles login and registration  
   |    |    |-- forms.py                  # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/                     # Templates used to render pages
   |         |-- includes/                 # HTML chunks and components
   |         |    |-- navigation.html      # Top menu component
   |         |    |-- sidebar.html         # Sidebar component
   |         |    |-- footer.html          # App Footer
   |         |    |-- scripts.html         # Scripts common to all pages
   |         |
   |         |-- layouts/                   # Master pages
   |         |    |-- base-fullscreen.html  # Used by Authentication pages
   |         |    |-- base.html             # Used by common pages
   |         |
   |         |-- accounts/                  # Authentication pages
   |         |    |-- login.html            # Login page
   |         |    |-- register.html         # Register page
   |         |
   |         |-- home/                      # UI Kit Pages
   |              |-- index.html            # Index page
   |              |-- 404-page.html         # 404 page
   |              |-- *.html                # All other pages
   |
   |-- requirements.txt                     # Development modules - SQLite storage
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- manage.py                            # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

## 📚 Libraries Used

- ✅ `Django` - Basic Web Framework and MVT design pattern
- ✅ `ReportLab` - Exporting in PDF format
- ✅ `Docx` Exporting in DOCX format for Word and Google Docs

## 🏋 리프핏

> One Rep Max 무게를 기반으로 Wendler 운동 시트 생성 웹앱
>
> 라이브 사이트 https://kyeongsupchoi.pythonanywhere.com
>
> Wendler 운동 프로그램 설명: https://www.t-nation.com/workouts/5-3-1-how-to-build-pure-strength/


<br />

## 📚 사용된 라이브러리

- ✅ `Django` - 기본 웹 프레임워크 및 MVT 디자인 패턴
- ✅ `ReportLab` - PDF 형식으로 다운로드
- ✅ `Docx` Word 및 Google 문서용 DOCX 형식으로 다운로드

<br />

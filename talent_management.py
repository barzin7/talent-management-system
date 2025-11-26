import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import numpy as np
from typing import Dict, List

# تنظیمات صفحه
st.set_page_config(
    page_title="سیستم مدیریت استعداد",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# عنوان اصلی
st.markdown("<h1 style='text-align: center; color: #1f4e78;'>👥 سیستم کامل مدیریت استعداد و توسعه کارکنان</h1>", 
            unsafe_allow_html=True)

# فایل ذخیره سازی داده‌ها
DATA_FILE = "complete_talent_data.xlsx"

class CompleteTalentSystem:
    def __init__(self):
        self.init_data()
    
    def init_data(self):
        """ایجاد ساختار اولیه داده‌ها با تمام جداول"""
        if not os.path.exists(DATA_FILE):
            # ۱. کارکنان
            employees_df = pd.DataFrame(columns=[
                'EmployeeID', 'FullName', 'Gender', 'BirthDate', 'HireDate',
                'JobCode', 'JobTitle', 'Unit', 'ManagerID', 'EducationLevel',
                'Major', 'Specialization', 'PersonalityType', 'InterviewScore',
                'SelfAssessmentScore', 'CareerStage', 'CareerStrategy', 
                'RoleResponsibilities', 'KPITargets', 'LearningPreferences',
                'MotivationScore', 'SuccessionPool'
            ])
            
            # ۲. ساختار سازمانی
            org_df = pd.DataFrame(columns=[
                'Level', 'Code', 'Title', 'ParentCode', 'ResponsibilityLevel',
                'UnitHead', 'NumberOfEmployees', 'DepartmentKPIs'
            ])
            
            # ۳. شایستگی‌ها
            competencies_df = pd.DataFrame(columns=[
                'JobCode', 'CompetencyCategory', 'CompetencyName', 
                'BehavioralIndicators', 'RequiredLevel', 'AssessmentMethod',
                'LinkedCourses', 'Priority'
            ])
            
            # ۴. شکاف‌ها
            gaps_df = pd.DataFrame(columns=[
                'GapID', 'EmployeeID', 'JobCode', 'Unit', 'GapType', 
                'GapName', 'Description', 'RequiredLevel', 'CurrentLevel',
                'GapSize', 'Urgency', 'ImpactOnTeam', 'ImpactOnOrg',
                'CostEstimate', 'RootCause', 'Dependencies', 'Owner',
                'SuccessMetric', 'Status'
            ])
            
            # ۵. برنامه‌های توسعه
            development_df = pd.DataFrame(columns=[
                'PlanID', 'GapID', 'PlanName', 'PlanType', 'Provider',
                'StartDate', 'EndDate', 'EstimatedHours', 'Cost', 'Owner',
                'TargetOutcome', 'EvaluationMethod', 'Progress', 'Status'
            ])
            
            # ۶. دوره‌های آموزشی
            courses_df = pd.DataFrame(columns=[
                'CourseID', 'CourseName', 'CourseType', 'Provider', 
                'DurationHours', 'Cost', 'LinkedCompetency', 'DeliveryType',
                'LevelExpectation', 'LevelAchieved'
            ])
            
            # ۷. سوابق آموزشی
            training_df = pd.DataFrame(columns=[
                'RecordID', 'EmployeeID', 'CourseID', 'AttendanceDate',
                'PreTestScore', 'PostTestScore', 'Improvement', 'Status'
            ])
            
            # ۸. شاخص‌های عملکرد
            kpi_df = pd.DataFrame(columns=[
                'KPIID', 'EmployeeID', 'KPIName', 'Date', 'Value', 
                'Target', 'Variance', 'Status', 'LinkedCompetency',
                'LinkedGapID', 'UnitLevelAggregation'
            ])
            
            # ذخیره در فایل اکسل
            with pd.ExcelWriter(DATA_FILE, engine='openpyxl') as writer:
                employees_df.to_excel(writer, sheet_name='Employees', index=False)
                org_df.to_excel(writer, sheet_name='Organization', index=False)
                competencies_df.to_excel(writer, sheet_name='Competencies', index=False)
                gaps_df.to_excel(writer, sheet_name='Gaps', index=False)
                development_df.to_excel(writer, sheet_name='Development_Plans', index=False)
                courses_df.to_excel(writer, sheet_name='Training_Courses', index=False)
                training_df.to_excel(writer, sheet_name='Training_Records', index=False)
                kpi_df.to_excel(writer, sheet_name='KPI', index=False)
    
    def load_sheet(self, sheet_name):
        """بارگذاری یک شیت از فایل اکسل"""
        try:
            return pd.read_excel(DATA_FILE, sheet_name=sheet_name)
        except Exception as e:
            st.error(f"خطا در بارگذاری شیت {sheet_name}: {e}")
            return pd.DataFrame()
    
    def save_sheet(self, df, sheet_name):
        """ذخیره یک شیت در فایل اکسل"""
        try:
            existing_data = {}
            try:
                existing_data = pd.read_excel(DATA_FILE, sheet_name=None)
            except:
                pass
                
            existing_data[sheet_name] = df
            with pd.ExcelWriter(DATA_FILE, engine='openpyxl') as writer:
                for sheet, data in existing_data.items():
                    data.to_excel(writer, sheet_name=sheet, index=False)
            return True
        except Exception as e:
            st.error(f"خطا در ذخیره‌سازی: {e}")
            return False
    
    def generate_complete_sample_data(self):
        """ایجاد داده‌های نمونه کامل"""
        # ۱. ساختار سازمانی
        org_data = [
            {
                'Level': 1, 'Code': 'ORG', 'Title': 'شرکت پارسیان', 'ParentCode': '',
                'ResponsibilityLevel': 'سازمان', 'UnitHead': 'CEO-001',
                'NumberOfEmployees': 500, 'DepartmentKPIs': 'سودآوری; رضایت مشتری'
            },
            {
                'Level': 2, 'Code': 'DEP01', 'Title': 'معاونت فناوری اطلاعات', 'ParentCode': 'ORG',
                'ResponsibilityLevel': 'معاونت', 'UnitHead': 'MGR-101',
                'NumberOfEmployees': 50, 'DepartmentKPIs': 'uptime سیستم‌ها; امنیت سایبری'
            },
            {
                'Level': 3, 'Code': 'UNIT01', 'Title': 'واحد توسعه نرم‌افزار', 'ParentCode': 'DEP01',
                'ResponsibilityLevel': 'واحد', 'UnitHead': 'MGR-201',
                'NumberOfEmployees': 15, 'DepartmentKPIs': 'تحویل به موقع پروژه‌ها; کیفیت کد'
            },
            {
                'Level': 3, 'Code': 'UNIT02', 'Title': 'واحد زیرساخت', 'ParentCode': 'DEP01',
                'ResponsibilityLevel': 'واحد', 'UnitHead': 'MGR-202',
                'NumberOfEmployees': 10, 'DepartmentKPIs': 'uptime سرورها; زمان پاسخگویی'
            }
        ]
        
        # ۲. کارکنان
        employees_data = [
            {
                'EmployeeID': 'EMP-001', 'FullName': 'علی محمدی', 'Gender': 'مرد',
                'BirthDate': '1985-03-15', 'HireDate': '2020-06-01', 'JobCode': 'J-DEV-SR',
                'JobTitle': 'توسعه‌دهنده ارشد', 'Unit': 'UNIT01', 'ManagerID': 'MGR-201',
                'EducationLevel': 'کارشناسی ارشد', 'Major': 'مهندسی نرم‌افزار',
                'Specialization': 'هوش مصنوعی', 'PersonalityType': 'INTJ', 'InterviewScore': 88,
                'SelfAssessmentScore': 4.2, 'CareerStage': 'حرفه‌ای',
                'CareerStrategy': 'تبدیل به معمار نرم‌افزار در ۳ سال آینده',
                'RoleResponsibilities': 'توسعه ماژول‌های پیچیده; منتورینگ جونیورها',
                'KPITargets': 'باگ کمتر از ۲%; تحویل ۱۰۰% وظایف',
                'LearningPreferences': 'آموزش آنلاین; کارگاه عملی',
                'MotivationScore': 8, 'SuccessionPool': 'جانشین لید تیم'
            },
            {
                'EmployeeID': 'EMP-002', 'FullName': 'فاطمه احمدی', 'Gender': 'زن',
                'BirthDate': '1992-08-22', 'HireDate': '2021-11-15', 'JobCode': 'J-DEV-JR',
                'JobTitle': 'توسعه‌دهنده جونیور', 'Unit': 'UNIT01', 'ManagerID': 'MGR-201',
                'EducationLevel': 'کارشناسی', 'Major': 'مهندسی کامپیوتر',
                'Specialization': 'نرم‌افزار', 'PersonalityType': 'ENFJ', 'InterviewScore': 82,
                'SelfAssessmentScore': 3.8, 'CareerStage': 'توسعه',
                'CareerStrategy': 'تبدیل به توسعه‌دهنده ارشد در ۲ سال',
                'RoleResponsibilities': 'توسعه ماژول‌های ساده; یادگیری فناوری‌های جدید',
                'KPITargets': 'یادگیری ۳ فناوری جدید; مشارکت در تیم',
                'LearningPreferences': 'منتورینگ; پروژه عملی',
                'MotivationScore': 7, 'SuccessionPool': 'توسعه‌دهنده ارشد'
            },
            {
                'EmployeeID': 'EMP-003', 'FullName': 'محمود رضایی', 'Gender': 'مرد',
                'BirthDate': '1988-11-05', 'HireDate': '2019-03-10', 'JobCode': 'J-NET-AD',
                'JobTitle': 'کارشناس شبکه', 'Unit': 'UNIT02', 'ManagerID': 'MGR-202',
                'EducationLevel': 'کارشناسی', 'Major': 'مهندسی IT',
                'Specialization': 'شبکه', 'PersonalityType': 'ISTJ', 'InterviewScore': 85,
                'SelfAssessmentScore': 4.0, 'CareerStage': 'حرفه‌ای',
                'CareerStrategy': 'تبدیل به مدیر شبکه در ۴ سال آینده',
                'RoleResponsibilities': 'مدیریت شبکه; پشتیبانی فنی',
                'KPITargets': ' uptime 99.9%; رضایت کاربران 95%',
                'LearningPreferences': 'دوره‌های تخصصی; گواهینامه‌ها',
                'MotivationScore': 9, 'SuccessionPool': 'مدیر شبکه'
            }
        ]
        
        # ۳. شایستگی‌ها
        competencies_data = [
            {
                'JobCode': 'J-DEV-SR', 'CompetencyCategory': 'فنی', 
                'CompetencyName': 'برنامه‌نویسی پیشرفته پایتون',
                'BehavioralIndicators': 'می‌تواند الگوریتم‌های پیچیده را پیاده‌سازی کند',
                'RequiredLevel': 5, 'AssessmentMethod': 'آزمون عملی',
                'LinkedCourses': 'C-PY-ADV', 'Priority': 'بالا'
            },
            {
                'JobCode': 'J-DEV-SR', 'CompetencyCategory': 'رفتاری',
                'CompetencyName': 'رهبری فنی',
                'BehavioralIndicators': 'می‌تواند به اعضای تیم راهنمایی فنی ارائه دهد',
                'RequiredLevel': 4, 'AssessmentMethod': 'ارزیابی ۳۶۰ درجه',
                'LinkedCourses': 'C-LEAD-MGT', 'Priority': 'متوسط'
            },
            {
                'JobCode': 'J-DEV-JR', 'CompetencyCategory': 'فنی',
                'CompetencyName': 'برنامه‌نویسی مقدماتی پایتون',
                'BehavioralIndicators': 'می‌تواند ماژول‌های ساده را توسعه دهد',
                'RequiredLevel': 3, 'AssessmentMethod': 'آزمون کتبی',
                'LinkedCourses': 'C-PY-BAS', 'Priority': 'بالا'
            },
            {
                'JobCode': 'J-NET-AD', 'CompetencyCategory': 'فنی',
                'CompetencyName': 'مدیریت شبکه‌های پیشرفته',
                'BehavioralIndicators': 'می‌تواند شبکه‌های پیچیده را طراحی و مدیریت کند',
                'RequiredLevel': 4, 'AssessmentMethod': 'آزمون عملی',
                'LinkedCourses': 'C-NET-ADV', 'Priority': 'بحرانی'
            }
        ]
        
        # ۴. شکاف‌ها
        gaps_data = [
            {
                'GapID': 'GAP-001', 'EmployeeID': 'EMP-002', 'JobCode': 'J-DEV-JR',
                'Unit': 'UNIT01', 'GapType': 'مهارتی', 'GapName': 'طراحی معماری',
                'Description': 'در طراحی معماری ماژول‌های مستقل مشکل دارد',
                'RequiredLevel': 3, 'CurrentLevel': 1, 'GapSize': 2,
                'Urgency': 'متوسط', 'ImpactOnTeam': 'بالا', 'ImpactOnOrg': 'متوسط',
                'CostEstimate': 5000000, 'RootCause': 'عدم تجربه; عدم آموزش',
                'Dependencies': 'تأیید مدیر', 'Owner': 'MGR-201',
                'SuccessMetric': 'نمره آزمون عملی به ۴ برسد', 'Status': 'جدید'
            },
            {
                'GapID': 'GAP-002', 'EmployeeID': 'EMP-001', 'JobCode': 'J-DEV-SR',
                'Unit': 'UNIT01', 'GapType': 'رفتاری', 'GapName': 'ارائه مؤثر',
                'Description': 'در ارائه یافته‌ها به مدیریت ضعف دارد',
                'RequiredLevel': 4, 'CurrentLevel': 2, 'GapSize': 2,
                'Urgency': 'پایین', 'ImpactOnTeam': 'متوسط', 'ImpactOnOrg': 'پایین',
                'CostEstimate': 2000000, 'RootCause': 'عدم اعتماد به نفس',
                'Dependencies': 'شرکت در کارگاه', 'Owner': 'MGR-201',
                'SuccessMetric': 'ارائه موفق به مدیریت ارشد', 'Status': 'در دست اقدام'
            },
            {
                'GapID': 'GAP-003', 'EmployeeID': 'EMP-003', 'JobCode': 'J-NET-AD',
                'Unit': 'UNIT02', 'GapType': 'مهارتی', 'GapName': 'امنیت شبکه',
                'Description': 'آشنایی کمی با پروتکل‌های امنیتی جدید دارد',
                'RequiredLevel': 4, 'CurrentLevel': 2, 'GapSize': 2,
                'Urgency': 'بالا', 'ImpactOnTeam': 'بالا', 'ImpactOnOrg': 'بالا',
                'CostEstimate': 3000000, 'RootCause': 'تغییر سریع فناوری',
                'Dependencies': 'آموزش تخصصی', 'Owner': 'MGR-202',
                'SuccessMetric': 'گواهینامه امنیت شبکه', 'Status': 'جدید'
            }
        ]
        
        # ۵. برنامه‌های توسعه
        development_data = [
            {
                'PlanID': 'PLAN-001', 'GapID': 'GAP-001', 'PlanName': 'دوره آموزشی معماری نرم‌افزار',
                'PlanType': 'آموزش', 'Provider': 'آکادمی داخلی', 'StartDate': '2024-08-01',
                'EndDate': '2024-08-15', 'EstimatedHours': 16, 'Cost': 2000000,
                'Owner': 'EMP-002', 'TargetOutcome': 'توانایی طراحی ماژول مستقل',
                'EvaluationMethod': 'ارزیابی عملی توسط لید تیم', 'Progress': 0, 'Status': 'برنامه‌ریزی شده'
            },
            {
                'PlanID': 'PLAN-002', 'GapID': 'GAP-002', 'PlanName': 'کارگاه مهارت‌های ارائه',
                'PlanType': 'آموزش', 'Provider': 'مؤسسه بیرونی', 'StartDate': '2024-07-10',
                'EndDate': '2024-07-11', 'EstimatedHours': 8, 'Cost': 1500000,
                'Owner': 'EMP-001', 'TargetOutcome': 'ارائه مؤثر به مدیریت',
                'EvaluationMethod': 'ارائه آزمایشی', 'Progress': 25, 'Status': 'در جریان'
            },
            {
                'PlanID': 'PLAN-003', 'GapID': 'GAP-003', 'PlanName': 'دوره تخصصی امنیت شبکه',
                'PlanType': 'آموزش', 'Provider': 'شرکت سیسکو', 'StartDate': '2024-09-01',
                'EndDate': '2024-09-30', 'EstimatedHours': 40, 'Cost': 5000000,
                'Owner': 'EMP-003', 'TargetOutcome': 'دریافت گواهینامه CCNA Security',
                'EvaluationMethod': 'آزمون بین‌المللی', 'Progress': 0, 'Status': 'برنامه‌ریزی شده'
            }
        ]
        
        # ۶. دوره‌های آموزشی
        courses_data = [
            {
                'CourseID': 'C-PY-ADV', 'CourseName': 'برنامه‌نویسی پیشرفته پایتون',
                'CourseType': 'حضوری', 'Provider': 'آکادمی داخلی', 'DurationHours': 24,
                'Cost': 1500000, 'LinkedCompetency': 'برنامه‌نویسی پیشرفته پایتون',
                'DeliveryType': 'کلاسی', 'LevelExpectation': 4, 'LevelAchieved': 0
            },
            {
                'CourseID': 'C-LEAD-MGT', 'CourseName': 'مدیریت و رهبری تیم',
                'CourseType': 'حضوری', 'Provider': 'مؤسسه بیرونی', 'DurationHours': 16,
                'Cost': 3000000, 'LinkedCompetency': 'رهبری فنی',
                'DeliveryType': 'کارگاهی', 'LevelExpectation': 4, 'LevelAchieved': 0
            },
            {
                'CourseID': 'C-PY-BAS', 'CourseName': 'برنامه‌نویسی مقدماتی پایتون',
                'CourseType': 'آنلاین', 'Provider': 'آکادمی داخلی', 'DurationHours': 20,
                'Cost': 800000, 'LinkedCompetency': 'برنامه‌نویسی مقدماتی پایتون',
                'DeliveryType': 'خودآموز', 'LevelExpectation': 3, 'LevelAchieved': 0
            },
            {
                'CourseID': 'C-NET-ADV', 'CourseName': 'مدیریت شبکه‌های پیشرفته',
                'CourseType': 'حضوری', 'Provider': 'شرکت سیسکو', 'DurationHours': 40,
                'Cost': 5000000, 'LinkedCompetency': 'مدیریت شبکه‌های پیشرفته',
                'DeliveryType': 'آزمایشگاهی', 'LevelExpectation': 4, 'LevelAchieved': 0
            }
        ]
        
        # ۷. KPI
        kpi_data = [
            {
                'KPIID': 'KPI-001', 'EmployeeID': 'EMP-001', 'KPIName': 'تعداد باگ در تولید',
                'Date': '2024-06-01', 'Value': 1, 'Target': 2, 'Variance': -1,
                'Status': 'سبز', 'LinkedCompetency': 'برنامه‌نویسی پیشرفته پایتون',
                'LinkedGapID': 'GAP-002', 'UnitLevelAggregation': '۹۸%'
            },
            {
                'KPIID': 'KPI-002', 'EmployeeID': 'EMP-001', 'KPIName': 'تحویل به موقع وظایف',
                'Date': '2024-06-01', 'Value': 95, 'Target': 100, 'Variance': -5,
                'Status': 'زرد', 'LinkedCompetency': 'رهبری فنی',
                'LinkedGapID': 'GAP-002', 'UnitLevelAggregation': '۹۵%'
            },
            {
                'KPIID': 'KPI-003', 'EmployeeID': 'EMP-002', 'KPIName': 'یادگیری فناوری جدید',
                'Date': '2024-06-01', 'Value': 2, 'Target': 3, 'Variance': -1,
                'Status': 'زرد', 'LinkedCompetency': 'برنامه‌نویسی مقدماتی پایتون',
                'LinkedGapID': 'GAP-001', 'UnitLevelAggregation': '۶۷%'
            },
            {
                'KPIID': 'KPI-004', 'EmployeeID': 'EMP-003', 'KPIName': ' uptime شبکه',
                'Date': '2024-06-01', 'Value': 99.8, 'Target': 99.5, 'Variance': 0.3,
                'Status': 'سبز', 'LinkedCompetency': 'مدیریت شبکه‌های پیشرفته',
                'LinkedGapID': 'GAP-003', 'UnitLevelAggregation': '۹۹.۸%'
            }
        ]
        
        # ذخیره تمام داده‌ها
        self.save_sheet(pd.DataFrame(org_data), 'Organization')
        self.save_sheet(pd.DataFrame(employees_data), 'Employees')
        self.save_sheet(pd.DataFrame(competencies_data), 'Competencies')
        self.save_sheet(pd.DataFrame(gaps_data), 'Gaps')
        self.save_sheet(pd.DataFrame(development_data), 'Development_Plans')
        self.save_sheet(pd.DataFrame(courses_data), 'Training_Courses')
        self.save_sheet(pd.DataFrame(kpi_data), 'KPI')
        
        st.success("✅ داده‌های نمونه کامل با موفقیت ایجاد شدند!")

# ایجاد نمونه از سیستم
tms = CompleteTalentSystem()

def show_comprehensive_dashboard():
    """داشبورد جامع با تمام متریک‌ها"""
    st.markdown("## 📊 داشبورد جامع مدیریت استعداد")
    
    # بارگذاری تمام داده‌ها
    employees_df = tms.load_sheet('Employees')
    gaps_df = tms.load_sheet('Gaps')
    development_df = tms.load_sheet('Development_Plans')
    kpi_df = tms.load_sheet('KPI')
    training_df = tms.load_sheet('Training_Records')
    
    # ردیف اول: کارت‌های کلیدی
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        total_employees = len(employees_df) if not employees_df.empty else 0
        st.metric("👥 کارکنان", total_employees, "نفر")
    
    with col2:
        total_gaps = len(gaps_df) if not gaps_df.empty else 0
        st.metric("🎯 شکاف‌ها", total_gaps, "مورد")
    
    with col3:
        critical_gaps = len(gaps_df[gaps_df['GapSize'] >= 2]) if not gaps_df.empty else 0
        st.metric("🚨 شکاف‌های بحرانی", critical_gaps, "مورد")
    
    with col4:
        active_plans = len(development_df[development_df['Status'] == 'در جریان']) if not development_df.empty else 0
        st.metric("📈 برنامه‌های فعال", active_plans, "برنامه")
    
    with col5:
        completed_plans = len(development_df[development_df['Status'] == 'تکمیل شده']) if not development_df.empty else 0
        st.metric("✅ برنامه‌های تکمیل شده", completed_plans, "برنامه")
    
    with col6:
        if not employees_df.empty and 'MotivationScore' in employees_df.columns:
            avg_motivation = employees_df['MotivationScore'].mean() 
        else:
            avg_motivation = 0
        st.metric("💪 میانگین انگیزه", f"{avg_motivation:.1f}", "/10")
    
    # ردیف دوم: نمودارها
    col1, col2 = st.columns(2)
    
    with col1:
        if not gaps_df.empty and 'GapType' in gaps_df.columns:
            # نمودار توزیع شکاف‌ها
            gap_type_dist = gaps_df['GapType'].value_counts()
            fig_gap_type = px.pie(
                values=gap_type_dist.values,
                names=gap_type_dist.index,
                title="توزیع انواع شکاف‌ها",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_gap_type, use_container_width=True)
    
    with col2:
        if not development_df.empty and 'Status' in development_df.columns:
            # نمودار وضعیت برنامه‌های توسعه
            status_dist = development_df['Status'].value_counts()
            fig_status = px.bar(
                x=status_dist.values,
                y=status_dist.index,
                title="وضعیت برنامه‌های توسعه",
                orientation='h',
                color=status_dist.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    # ردیف سوم: تحلیل‌های پیشرفته
    col1, col2 = st.columns(2)
    
    with col1:
        if not gaps_df.empty and not employees_df.empty and 'Unit' in employees_df.columns:
            # شکاف‌ها به تفکیک واحد
            gap_analysis = gaps_df.merge(
                employees_df[['EmployeeID', 'Unit']], 
                on='EmployeeID', how='left'
            )
            if not gap_analysis.empty and 'Unit' in gap_analysis.columns:
                unit_gaps = gap_analysis.groupby('Unit').size()
                fig_unit_gaps = px.bar(
                    x=unit_gaps.values,
                    y=unit_gaps.index,
                    title="تعداد شکاف‌ها به تفکیک واحد",
                    orientation='h',
                    color=unit_gaps.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_unit_gaps, use_container_width=True)
    
    with col2:
        if not kpi_df.empty and 'Status' in kpi_df.columns:
            # عملکرد KPI
            kpi_status = kpi_df['Status'].value_counts()
            fig_kpi = px.pie(
                values=kpi_status.values,
                names=kpi_status.index,
                title="وضعیت شاخص‌های عملکرد (KPI)",
                color_discrete_sequence=['#00ff00', '#ffff00', '#ff0000']
            )
            st.plotly_chart(fig_kpi, use_container_width=True)
    
    # ردیف چهارم: تحلیل‌های عمیق‌تر
    col1, col2 = st.columns(2)
    
    with col1:
        if not gaps_df.empty and 'Urgency' in gaps_df.columns and 'ImpactOnTeam' in gaps_df.columns:
            # ماتریس فوریت-تأثیر
            urgency_order = ['کم', 'متوسط', 'زیاد']
            impact_order = ['کم', 'متوسط', 'زیاد']
            
            # ایجاد ماتریس
            matrix_data = []
            for urgency in urgency_order:
                for impact in impact_order:
                    count = len(gaps_df[(gaps_df['Urgency'] == urgency) & 
                                      (gaps_df['ImpactOnTeam'] == impact)])
                    matrix_data.append({'فوریت': urgency, 'تأثیر': impact, 'تعداد': count})
            
            matrix_df = pd.DataFrame(matrix_data)
            
            if not matrix_df.empty:
                fig_matrix = px.density_heatmap(
                    matrix_df, 
                    x='فوریت', 
                    y='تأثیر', 
                    z='تعداد',
                    title="ماتریس فوریت-تأثیر شکاف‌ها",
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig_matrix, use_container_width=True)
    
    with col2:
        if not employees_df.empty and 'CareerStage' in employees_df.columns and 'MotivationScore' in employees_df.columns:
            # تحلیل مراحل شغلی
            stage_analysis = employees_df.groupby('CareerStage').agg({
                'MotivationScore': 'mean',
                'EmployeeID': 'count'
            }).reset_index()
            
            fig_stage = px.scatter(
                stage_analysis,
                x='MotivationScore',
                y='CareerStage',
                size='EmployeeID',
                color='MotivationScore',
                title="تحلیل انگیزه بر اساس مرحله شغلی",
                size_max=40
            )
            st.plotly_chart(fig_stage, use_container_width=True)

def employee_management():
    """مدیریت کامل کارکنان"""
    st.markdown("## 👥 مدیریت کارکنان")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 لیست کارکنان", "➕ افزودن کارمند", "✏️ ویرایش اطلاعات", "📊 تحلیل کارکنان"])
    
    with tab1:
        show_employees_list()
    
    with tab2:
        add_employee_form()
    
    with tab3:
        edit_employee_form()
    
    with tab4:
        analyze_employees()

def show_employees_list():
    """نمایش لیست کارکنان"""
    employees_df = tms.load_sheet('Employees')
    
    if not employees_df.empty:
        # فیلترها
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            units = ['همه'] + list(employees_df['Unit'].unique()) if 'Unit' in employees_df.columns else ['همه']
            selected_unit = st.selectbox("فیلتر بر اساس واحد", units)
        
        with col2:
            if 'CareerStage' in employees_df.columns:
                career_stages = ['همه'] + list(employees_df['CareerStage'].unique()) 
            else:
                career_stages = ['همه']
            selected_stage = st.selectbox("فیلتر بر اساس مرحله شغلی", career_stages)
        
        with col3:
            if 'EducationLevel' in employees_df.columns:
                education_levels = ['همه'] + list(employees_df['EducationLevel'].unique())
            else:
                education_levels = ['همه']
            selected_edu = st.selectbox("فیلتر بر اساس تحصیلات", education_levels)
        
        with col4:
            if 'SuccessionPool' in employees_df.columns:
                succession_pools = ['همه'] + list(employees_df['SuccessionPool'].unique())
            else:
                succession_pools = ['همه']
            selected_pool = st.selectbox("فیلتر بر اساس جانشین‌پروری", succession_pools)
        
        # اعمال فیلترها
        filtered_df = employees_df.copy()
        if selected_unit != 'همه' and 'Unit' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Unit'] == selected_unit]
        if selected_stage != 'همه' and 'CareerStage' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['CareerStage'] == selected_stage]
        if selected_edu != 'همه' and 'EducationLevel' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['EducationLevel'] == selected_edu]
        if selected_pool != 'همه' and 'SuccessionPool' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['SuccessionPool'] == selected_pool]
        
        # نمایش آمار
        st.info(f"📊 نمایش {len(filtered_df)} کارمند از {len(employees_df)} کارمند")
        
        # انتخاب ستون‌ها برای نمایش
        display_columns = ['EmployeeID', 'FullName', 'Gender', 'JobTitle', 'Unit', 
                          'EducationLevel', 'CareerStage', 'MotivationScore', 'SuccessionPool']
        
        # حذف ستون‌هایی که وجود ندارند
        display_columns = [col for col in display_columns if col in filtered_df.columns]
        
        # نمایش جدول
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True
        )
        
        # دکمه دانلود
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 دانلود خروجی CSV",
            data=csv,
            file_name=f"employees_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("📝 هنوز کارمندی ثبت نشده است.")

def add_employee_form():
    """فرم افزودن کارمند جدید"""
    st.subheader("افزودن کارمند جدید")
    
    with st.form("add_employee_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            employee_id = st.text_input("کد پرسنلی *", placeholder="EMP-1001")
            full_name = st.text_input("نام کامل *", placeholder="رضا محمدی")
            gender = st.selectbox("جنسیت *", ["", "مرد", "زن"])
            birth_date = st.date_input("تاریخ تولد *", value=datetime.now())
            hire_date = st.date_input("تاریخ استخدام *", value=datetime.now())
            job_code = st.text_input("کد شغلی", placeholder="J-DEV-SR")
        
        with col2:
            job_title = st.text_input("عنوان شغل", placeholder="توسعه‌دهنده ارشد")
            unit = st.selectbox("واحد *", [
                "", "UNIT01", "UNIT02", "UNIT03", "سایر"
            ])
            manager_id = st.text_input("کد مدیر", placeholder="MGR-001")
            education_level = st.selectbox("مقطع تحصیلی", [
                "", "دیپلم", "کاردانی", "کارشناسی", "کارشناسی ارشد", "دکتری"
            ])
            major = st.text_input("رشته تحصیلی", placeholder="مهندسی نرم‌افزار")
            specialization = st.text_input("گرایش", placeholder="هوش مصنوعی")
        
        col3, col4 = st.columns(2)
        with col3:
            personality_type = st.text_input("تیپ شخصیتی", placeholder="INTJ")
            interview_score = st.slider("نمره مصاحبه", 0, 100, 70)
            self_assessment_score = st.slider("خوداظهاری", 1.0, 5.0, 3.0)
            career_stage = st.selectbox("مرحله رشد شغلی", [
                "", "تازه‌کار", "در حال توسعه", "حرفه‌ای", "ارشد", "کارشناس"
            ])
        
        with col4:
            career_strategy = st.text_area("استراتژی رشد فردی", placeholder="اهداف شغلی و برنامه توسعه...")
            role_responsibilities = st.text_area("مسئولیت‌های نقش", placeholder="وظایف و مسئولیت‌های شغلی...")
            kpi_targets = st.text_area("اهداف KPI", placeholder="شاخص‌های عملکرد و اهداف...")
            learning_preferences = st.text_input("ترجیحات یادگیری", placeholder="آموزش آنلاین، کارگاه، منتورینگ...")
        
        col5, col6 = st.columns(2)
        with col5:
            motivation_score = st.slider("نمره انگیزه", 1, 10, 7)
        
        with col6:
            succession_pool = st.text_input("جایگاه جانشین‌پروری", placeholder="لید تیم، مدیر واحد...")
        
        submitted = st.form_submit_button("💾 ذخیره اطلاعات کارمند")
        
        if submitted:
            if employee_id and full_name and gender and unit:
                employees_df = tms.load_sheet('Employees')
                
                # بررسی تکراری نبودن کد پرسنلی
                if not employees_df.empty and employee_id in employees_df['EmployeeID'].values:
                    st.error("❌ این کد پرسنلی قبلاً ثبت شده است!")
                else:
                    new_employee = {
                        'EmployeeID': employee_id,
                        'FullName': full_name,
                        'Gender': gender,
                        'BirthDate': birth_date.strftime('%Y-%m-%d'),
                        'HireDate': hire_date.strftime('%Y-%m-%d'),
                        'JobCode': job_code,
                        'JobTitle': job_title,
                        'Unit': unit,
                        'ManagerID': manager_id,
                        'EducationLevel': education_level,
                        'Major': major,
                        'Specialization': specialization,
                        'PersonalityType': personality_type,
                        'InterviewScore': interview_score,
                        'SelfAssessmentScore': self_assessment_score,
                        'CareerStage': career_stage,
                        'CareerStrategy': career_strategy,
                        'RoleResponsibilities': role_responsibilities,
                        'KPITargets': kpi_targets,
                        'LearningPreferences': learning_preferences,
                        'MotivationScore': motivation_score,
                        'SuccessionPool': succession_pool
                    }
                    
                    if employees_df.empty:
                        employees_df = pd.DataFrame([new_employee])
                    else:
                        employees_df = pd.concat([employees_df, pd.DataFrame([new_employee])], ignore_index=True)
                    
                    if tms.save_sheet(employees_df, 'Employees'):
                        st.success("✅ اطلاعات کارمند با موفقیت ذخیره شد!")
                        st.balloons()
            else:
                st.error("❌ لطفاً فیلدهای اجباری (ستاره‌دار) را پر کنید")

def edit_employee_form():
    """فرم ویرایش اطلاعات کارمند"""
    st.subheader("ویرایش اطلاعات کارمند")
    
    employees_df = tms.load_sheet('Employees')
    
    if not employees_df.empty:
        employee_ids = [''] + list(employees_df['EmployeeID'].unique())
        selected_emp = st.selectbox("انتخاب کارمند برای ویرایش", employee_ids)
        
        if selected_emp:
            employee_data = employees_df[employees_df['EmployeeID'] == selected_emp].iloc[0]
            
            with st.form("edit_employee_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    full_name = st.text_input("نام کامل", value=employee_data['FullName'])
                    job_title = st.text_input("عنوان شغل", value=employee_data['JobTitle'])
                    unit_options = ["UNIT01", "UNIT02", "UNIT03", "سایر"]
                    unit_index = unit_options.index(employee_data['Unit']) if employee_data['Unit'] in unit_options else 0
                    unit = st.selectbox("واحد", unit_options, index=unit_index)
                    
                    edu_options = ["دیپلم", "کاردانی", "کارشناسی", "کارشناسی ارشد", "دکتری"]
                    if employee_data['EducationLevel'] in edu_options:
                        edu_index = edu_options.index(employee_data['EducationLevel'])
                    else:
                        edu_index = 2  # کارشناسی به عنوان پیش‌فرض
                    education_level = st.selectbox("مقطع تحصیلی", edu_options, index=edu_index)
                
                with col2:
                    stage_options = ["تازه‌کار", "در حال توسعه", "حرفه‌ای", "ارشد", "کارشناس"]
                    if employee_data['CareerStage'] in stage_options:
                        stage_index = stage_options.index(employee_data['CareerStage'])
                    else:
                        stage_index = 2  # حرفه‌ای به عنوان پیش‌فرض
                    career_stage = st.selectbox("مرحله رشد شغلی", stage_options, index=stage_index)
                    
                    motivation_score = st.slider("نمره انگیزه", 1, 10, 
                                               value=int(employee_data['MotivationScore']) if pd.notna(employee_data['MotivationScore']) else 7)
                    succession_pool = st.text_input("جایگاه جانشین‌پروری", 
                                                  value=employee_data['SuccessionPool'] if pd.notna(employee_data['SuccessionPool']) else "")
                
                career_strategy = st.text_area("استراتژی رشد فردی", 
                                             value=employee_data['CareerStrategy'] if pd.notna(employee_data['CareerStrategy']) else "")
                
                submitted = st.form_submit_button("💾 به‌روزرسانی اطلاعات")
                
                if submitted:
                    # به‌روزرسانی داده‌ها
                    employees_df.loc[employees_df['EmployeeID'] == selected_emp, 'FullName'] = full_name
                    employees_df.loc[employees_df['EmployeeID'] == selected_emp, 'JobTitle'] = job_title
                    employees_df.loc[employees_df['EmployeeID'] == selected_emp, 'Unit'] = unit
                    employees_df.loc[employees_df['EmployeeID'] == selected_emp, 'EducationLevel'] = education_level
                    employees_df.loc[employees_df['EmployeeID'] == selected_emp, 'CareerStage'] = career_stage
                    employees_df.loc[employees_df['EmployeeID'] == selected_emp, 'MotivationScore'] = motivation_score
                    employees_df.loc[employees_df['EmployeeID'] == selected_emp, 'SuccessionPool'] = succession_pool
                    employees_df.loc[employees_df['EmployeeID'] == selected_emp, 'CareerStrategy'] = career_strategy
                    
                    if tms.save_sheet(employees_df, 'Employees'):
                        st.success("✅ اطلاعات کارمند با موفقیت به‌روزرسانی شد!")
    else:
        st.info("📝 هیچ کارمندی برای ویرایش وجود ندارد.")

def analyze_employees():
    """تحلیل پیشرفته کارکنان"""
    st.subheader("📊 تحلیل پیشرفته کارکنان")
    
    employees_df = tms.load_sheet('Employees')
    gaps_df = tms.load_sheet('Gaps')
    kpi_df = tms.load_sheet('KPI')
    
    if not employees_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # تحلیل انگیزه و عملکرد
            if 'MotivationScore' in employees_df.columns:
                fig_motivation = px.histogram(
                    employees_df, 
                    x='MotivationScore',
                    title="توزیع نمره انگیزه کارکنان",
                    nbins=10,
                    color_discrete_sequence=['#1f77b4']
                )
                st.plotly_chart(fig_motivation, use_container_width=True)
            
            # تحلیل مراحل شغلی
            if 'CareerStage' in employees_df.columns:
                stage_dist = employees_df['CareerStage'].value_counts()
                fig_stage = px.pie(
                    values=stage_dist.values,
                    names=stage_dist.index,
                    title="توزیع مراحل شغلی"
                )
                st.plotly_chart(fig_stage, use_container_width=True)
        
        with col2:
            # تحلیل تحصیلات
            if 'EducationLevel' in employees_df.columns:
                edu_dist = employees_df['EducationLevel'].value_counts()
                fig_edu = px.bar(
                    x=edu_dist.values,
                    y=edu_dist.index,
                    title="توزیع سطح تحصیلات",
                    orientation='h'
                )
                st.plotly_chart(fig_edu, use_container_width=True)
            
            # تحلیل جانشین‌پروری
            if 'SuccessionPool' in employees_df.columns:
                succession_dist = employees_df[employees_df['SuccessionPool'] != '']['SuccessionPool'].value_counts()
                if not succession_dist.empty:
                    fig_succession = px.bar(
                        x=succession_dist.values,
                        y=succession_dist.index,
                        title="توزیع جایگاه‌های جانشین‌پروری",
                        orientation='h'
                    )
                    st.plotly_chart(fig_succession, use_container_width=True)
        
        # تحلیل ترکیبی
        if not gaps_df.empty and not employees_df.empty:
            st.subheader("تحلیل شکاف‌های مهارتی کارکنان")
            
            # ارتباط داده‌ها
            employee_gaps = gaps_df.merge(
                employees_df[['EmployeeID', 'FullName', 'Unit', 'CareerStage']],
                on='EmployeeID', how='left'
            )
            
            # شکاف‌ها به تفکیک مرحله شغلی
            if not employee_gaps.empty and 'CareerStage' in employee_gaps.columns:
                stage_gap_analysis = employee_gaps.groupby('CareerStage').agg({
                    'GapSize': 'mean',
                    'GapID': 'count'
                }).reset_index()
                
                fig_stage_gap = px.scatter(
                    stage_gap_analysis,
                    x='GapSize',
                    y='CareerStage',
                    size='GapID',
                    color='GapSize',
                    title="میانگین شکاف مهارتی بر اساس مرحله شغلی",
                    size_max=40
                )
                st.plotly_chart(fig_stage_gap, use_container_width=True)
    else:
        st.info("📊 داده‌ای برای تحلیل وجود ندارد")

def gap_management():
    """مدیریت کامل شکاف‌ها"""
    st.markdown("## 🎯 مدیریت شکاف‌های مهارتی")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 شکاف‌ها", "➕ شکاف جدید", "📊 تحلیل شکاف", "🔗 ارتباط با برنامه توسعه", "🚨 شکاف‌های بحرانی"])
    
    with tab1:
        show_gaps_list()
    
    with tab2:
        add_gap_form()
    
    with tab3:
        show_gap_analysis()
    
    with tab4:
        link_gap_development()
    
    with tab5:
        show_critical_gaps()

def show_gaps_list():
    """نمایش لیست شکاف‌ها"""
    gaps_df = tms.load_sheet('Gaps')
    employees_df = tms.load_sheet('Employees')
    competencies_df = tms.load_sheet('Competencies')
    
    if not gaps_df.empty:
        # فیلترها
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            gap_types = ['همه'] + list(gaps_df['GapType'].unique()) if 'GapType' in gaps_df.columns else ['همه']
            selected_type = st.selectbox("نوع شکاف", gap_types)
        
        with col2:
            urgency_levels = ['همه'] + list(gaps_df['Urgency'].unique()) if 'Urgency' in gaps_df.columns else ['همه']
            selected_urgency = st.selectbox("فوریت", urgency_levels)
        
        with col3:
            statuses = ['همه'] + list(gaps_df['Status'].unique()) if 'Status' in gaps_df.columns else ['همه']
            selected_status = st.selectbox("وضعیت", statuses)
        
        with col4:
            gap_sizes = ['همه', 'کم (1)', 'متوسط (2)', 'زیاد (3+)']
            selected_size = st.selectbox("اندازه شکاف", gap_sizes)
        
        # اعمال فیلترها
        filtered_df = gaps_df.copy()
        if selected_type != 'همه' and 'GapType' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['GapType'] == selected_type]
        if selected_urgency != 'همه' and 'Urgency' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Urgency'] == selected_urgency]
        if selected_status != 'همه' and 'Status' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Status'] == selected_status]
        if selected_size != 'همه' and 'GapSize' in filtered_df.columns:
            if selected_size == 'کم (1)':
                filtered_df = filtered_df[filtered_df['GapSize'] == 1]
            elif selected_size == 'متوسط (2)':
                filtered_df = filtered_df[filtered_df['GapSize'] == 2]
            elif selected_size == 'زیاد (3+)':
                filtered_df = filtered_df[filtered_df['GapSize'] >= 3]
        
        # ارتباط با اطلاعات کارمند
        if not employees_df.empty and 'EmployeeID' in employees_df.columns:
            filtered_df = filtered_df.merge(
                employees_df[['EmployeeID', 'FullName', 'JobTitle', 'Unit']],
                on='EmployeeID', how='left'
            )
        
        st.info(f"📊 نمایش {len(filtered_df)} شکاف از {len(gaps_df)} شکاف")
        
        # نمایش جدول
        display_columns = ['FullName', 'JobTitle', 'Unit', 'GapName', 'GapType', 
                          'CurrentLevel', 'RequiredLevel', 'GapSize', 'Urgency', 'Status']
        
        # حذف ستون‌هایی که وجود ندارند
        display_columns = [col for col in display_columns if col in filtered_df.columns]
        
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True
        )
        
    else:
        st.info("📝 هنوز شکافی ثبت نشده است.")

def add_gap_form():
    """فرم ثبت شکاف جدید"""
    st.subheader("ثبت شکاف مهارتی جدید")
    
    employees_df = tms.load_sheet('Employees')
    competencies_df = tms.load_sheet('Competencies')
    
    if not employees_df.empty:
        with st.form("add_gap_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                employee_id = st.selectbox("کارمند *", employees_df['EmployeeID'].unique())
                employee_info = employees_df[employees_df['EmployeeID'] == employee_id].iloc[0]
                st.write(f"**شغل:** {employee_info['JobTitle']}")
                st.write(f"**واحد:** {employee_info['Unit']}")
                
                gap_name = st.text_input("عنوان شکاف *", placeholder="طراحی معماری")
                gap_type = st.selectbox("نوع شکاف *", ["مهارتی", "رفتاری", "فرهنگی", "انگیزشی"])
                description = st.text_area("شرح شکاف", placeholder="توضیح کامل درباره شکاف...")
            
            with col2:
                required_level = st.slider("سطح مورد نیاز *", 1, 5, 3)
                current_level = st.slider("سطح فعلی *", 1, 5, 1)
                gap_size = required_level - current_level
                
                st.write(f"**اندازه شکاف:** {gap_size}")
                
                urgency = st.selectbox("فوریت *", ["کم", "متوسط", "زیاد"])
                impact_team = st.selectbox("تأثیر بر تیم", ["کم", "متوسط", "زیاد"])
                impact_org = st.selectbox("تأثیر بر سازمان", ["کم", "متوسط", "زیاد"])
            
            col3, col4 = st.columns(2)
            with col3:
                root_cause = st.selectbox("علت ریشه‌ای", [
                    "عدم آموزش", "عدم تجربه", "عدم علاقه", 
                    "مشکل انگیزشی", "فقدان راهنمایی", "سایر"
                ])
                cost_estimate = st.number_input("برآورد هزینه (ریال)", min_value=0, value=0)
            
            with col4:
                owner = st.text_input("مالک پیگیری", placeholder="کد پرسنلی مدیر")
                success_metric = st.text_input("معیار موفقیت", placeholder="نمره آزمون به ۴ برسد")
                status = st.selectbox("وضعیت", ["جدید", "در دست اقدام", "در حال پیگیری", "حل شده"])
            
            submitted = st.form_submit_button("💾 ثبت شکاف")
            
            if submitted:
                if employee_id and gap_name:
                    gaps_df = tms.load_sheet('Gaps')
                    
                    new_gap = {
                        'GapID': f"GAP-{len(gaps_df) + 1:03d}",
                        'EmployeeID': employee_id,
                        'JobCode': employee_info['JobCode'] if 'JobCode' in employee_info else '',
                        'Unit': employee_info['Unit'],
                        'GapType': gap_type,
                        'GapName': gap_name,
                        'Description': description,
                        'RequiredLevel': required_level,
                        'CurrentLevel': current_level,
                        'GapSize': gap_size,
                        'Urgency': urgency,
                        'ImpactOnTeam': impact_team,
                        'ImpactOnOrg': impact_org,
                        'CostEstimate': cost_estimate,
                        'RootCause': root_cause,
                        'Dependencies': '',
                        'Owner': owner,
                        'SuccessMetric': success_metric,
                        'Status': status
                    }
                    
                    if gaps_df.empty:
                        gaps_df = pd.DataFrame([new_gap])
                    else:
                        gaps_df = pd.concat([gaps_df, pd.DataFrame([new_gap])], ignore_index=True)
                    
                    if tms.save_sheet(gaps_df, 'Gaps'):
                        st.success("✅ شکاف جدید با موفقیت ثبت شد!")
                        st.balloons()
                else:
                    st.error("❌ لطفاً فیلدهای اجباری را پر کنید")
    else:
        st.error("❌ ابتدا کارمند تعریف کنید")

def show_gap_analysis():
    """تحلیل پیشرفته شکاف‌ها"""
    st.subheader("📊 تحلیل پیشرفته شکاف‌ها")
    
    gaps_df = tms.load_sheet('Gaps')
    employees_df = tms.load_sheet('Employees')
    
    if not gaps_df.empty:
        # تحلیل سطح واحد
        col1, col2 = st.columns(2)
        
        with col1:
            # شکاف‌ها به تفکیک واحد و نوع
            if not employees_df.empty and 'Unit' in employees_df.columns:
                gap_analysis = gaps_df.merge(
                    employees_df[['EmployeeID', 'Unit']], 
                    on='EmployeeID', how='left'
                )
                
                if not gap_analysis.empty and 'Unit' in gap_analysis.columns and 'GapType' in gap_analysis.columns:
                    unit_gap_type = pd.crosstab(
                        gap_analysis['Unit'], 
                        gap_analysis['GapType']
                    )
                    
                    fig_unit_gap = px.bar(
                        unit_gap_type,
                        title="توزیع شکاف‌ها بر اساس واحد و نوع",
                        barmode='group'
                    )
                    st.plotly_chart(fig_unit_gap, use_container_width=True)
        
        with col2:
            # نمودار فوریت شکاف‌ها
            if 'Urgency' in gaps_df.columns and 'ImpactOnTeam' in gaps_df.columns:
                urgency_impact = pd.crosstab(
                    gaps_df['Urgency'],
                    gaps_df['ImpactOnTeam']
                )
                
                fig_urgency = px.imshow(
                    urgency_impact,
                    title="ماتریس فوریت-تأثیر شکاف‌ها",
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig_urgency, use_container_width=True)
        
        # تحلیل هزینه‌ها
        col3, col4 = st.columns(2)
        
        with col3:
            # توزیع هزینه‌های برآورد شده
            if 'CostEstimate' in gaps_df.columns and 'GapType' in gaps_df.columns:
                cost_analysis = gaps_df.groupby('GapType')['CostEstimate'].sum()
                if not cost_analysis.empty:
                    fig_cost = px.pie(
                        values=cost_analysis.values,
                        names=cost_analysis.index,
                        title="توزیع هزینه‌های برآورد شده بر اساس نوع شکاف"
                    )
                    st.plotly_chart(fig_cost, use_container_width=True)
        
        with col4:
            # تحلیل ریشه‌های علل
            if 'RootCause' in gaps_df.columns:
                root_cause_analysis = gaps_df['RootCause'].value_counts()
                if not root_cause_analysis.empty:
                    fig_root_cause = px.bar(
                        x=root_cause_analysis.values,
                        y=root_cause_analysis.index,
                        title="توزیع علل ریشه‌ای شکاف‌ها",
                        orientation='h'
                    )
                    st.plotly_chart(fig_root_cause, use_container_width=True)
        
    else:
        st.info("📊 داده‌ای برای تحلیل وجود ندارد")

def show_critical_gaps():
    """نمایش شکاف‌های بحرانی"""
    st.subheader("🚨 شکاف‌های بحرانی (Gap ≥ 2)")
    
    gaps_df = tms.load_sheet('Gaps')
    employees_df = tms.load_sheet('Employees')
    development_df = tms.load_sheet('Development_Plans')
    
    if not gaps_df.empty and 'GapSize' in gaps_df.columns:
        critical_gaps = gaps_df[gaps_df['GapSize'] >= 2]
        
        if not critical_gaps.empty:
            # ارتباط با اطلاعات کارمند
            if not employees_df.empty and 'EmployeeID' in employees_df.columns:
                # فقط ستون‌های موجود را انتخاب می‌کنیم
                employee_columns = ['EmployeeID', 'FullName', 'JobTitle', 'ManagerID']
                # فقط ستون‌هایی که وجود دارند را اضافه می‌کنیم
                available_columns = [col for col in employee_columns if col in employees_df.columns]
                
                if available_columns:
                    critical_gaps = critical_gaps.merge(
                        employees_df[available_columns],
                        on='EmployeeID', how='left'
                    )
            
            # ارتباط با برنامه‌های توسعه
            if not development_df.empty and 'GapID' in development_df.columns:
                development_columns = ['GapID', 'PlanName', 'Status', 'Progress']
                available_dev_columns = [col for col in development_columns if col in development_df.columns]
                
                if available_dev_columns:
                    critical_gaps = critical_gaps.merge(
                        development_df[available_dev_columns],
                        on='GapID', how='left'
                    )
            
            st.info(f"🔴 تعداد شکاف‌های بحرانی: {len(critical_gaps)}")
            
            for _, gap in critical_gaps.iterrows():
                # ایجاد عنوان ایمن
                employee_name = gap.get('FullName', 'نامشخص')
                gap_name = gap.get('GapName', 'نامشخص')
                gap_size = gap.get('GapSize', 0)
                
                with st.expander(f"🔴 {employee_name} - {gap_name} (شکاف: {gap_size})", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**اطلاعات پایه:**")
                        st.write(f"👤 کارمند: {employee_name}")
                        st.write(f"🏢 واحد: {gap.get('Unit', 'نامشخص')}")
                        st.write(f"💼 شغل: {gap.get('JobTitle', 'نامشخص')}")
                        st.write(f"🎯 نوع شکاف: {gap.get('GapType', 'نامشخص')}")
                    
                    with col2:
                        st.write("**سطح‌بندی:**")
                        st.write(f"📊 سطح فعلی: {gap.get('CurrentLevel', 'نامشخص')}")
                        st.write(f"🎯 سطح مورد نیاز: {gap.get('RequiredLevel', 'نامشخص')}")
                        st.write(f"📏 اندازه شکاف: {gap_size}")
                        st.write(f"⏰ فوریت: {gap.get('Urgency', 'نامشخص')}")
                    
                    with col3:
                        st.write("**تأثیرات:**")
                        st.write(f"👥 تأثیر بر تیم: {gap.get('ImpactOnTeam', 'نامشخص')}")
                        st.write(f"🏢 تأثیر بر سازمان: {gap.get('ImpactOnOrg', 'نامشخص')}")
                        cost = gap.get('CostEstimate', 0)
                        st.write(f"💰 برآورد هزینه: {cost:,} ریال")
                        st.write(f"🔍 علت ریشه‌ای: {gap.get('RootCause', 'نامشخص')}")
                    
                    # نمایش پیشرفت اگر برنامه توسعه وجود دارد
                    plan_name = gap.get('PlanName')
                    if pd.notna(plan_name) and plan_name:
                        st.write("**📋 برنامه توسعه مرتبط:**")
                        st.write(f"📝 برنامه: {plan_name}")
                        st.write(f"📈 وضعیت: {gap.get('Status', 'نامشخص')}")
                        progress = gap.get('Progress', 0)
                        st.write(f"📊 پیشرفت: {progress}%")
                        st.progress(progress / 100)
                    else:
                        st.warning("⚠️ هیچ برنامه توسعه‌ای برای این شکاف تعریف نشده است!")
                    
                    # نمایش نوار پیشرفت شکاف
                    st.write("**پیشرفت رفع شکاف:**")
                    current_level = gap.get('CurrentLevel', 0)
                    required_level = gap.get('RequiredLevel', 1)
                    if required_level > 0:
                        progress_percentage = (current_level / required_level) * 100
                    else:
                        progress_percentage = 0
                    st.progress(progress_percentage / 100)
                    st.write(f"پیشرفت: {progress_percentage:.1f}%")
            
            # خلاصه آماری
            st.subheader("📈 خلاصه آماری شکاف‌های بحرانی")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_cost = critical_gaps['CostEstimate'].sum() if 'CostEstimate' in critical_gaps.columns else 0
                st.metric("💰 مجموع هزینه‌های برآورد شده", f"{total_cost:,} ریال")
            
            with col2:
                avg_gap_size = critical_gaps['GapSize'].mean() if 'GapSize' in critical_gaps.columns else 0
                st.metric("📏 میانگین اندازه شکاف", f"{avg_gap_size:.1f}")
            
            with col3:
                if 'Urgency' in critical_gaps.columns:
                    high_urgency = len(critical_gaps[critical_gaps['Urgency'] == 'زیاد'])
                else:
                    high_urgency = 0
                st.metric("⏰ شکاف‌های با فوریت زیاد", high_urgency)
            
            with col4:
                if 'ImpactOnOrg' in critical_gaps.columns:
                    high_impact = len(critical_gaps[critical_gaps['ImpactOnOrg'] == 'زیاد'])
                else:
                    high_impact = 0
                st.metric("🏢 شکاف‌های با تأثیر سازمانی زیاد", high_impact)
                
        else:
            st.success("✅ هیچ شکاف بحرانی وجود ندارد!")
    else:
        st.info("📝 هیچ شکافی برای نمایش وجود ندارد")

def link_gap_development():
    """ارتباط شکاف‌ها با برنامه‌های توسعه"""
    st.subheader("🔗 ارتباط شکاف‌ها با برنامه‌های توسعه")
    
    gaps_df = tms.load_sheet('Gaps')
    development_df = tms.load_sheet('Development_Plans')
    employees_df = tms.load_sheet('Employees')
    courses_df = tms.load_sheet('Training_Courses')
    
    if not gaps_df.empty:
        # انتخاب شکاف برای ایجاد برنامه توسعه
        gap_options = {f"{row['GapID']} - {row['GapName']}": row['GapID'] 
                      for _, row in gaps_df.iterrows()}
        
        selected_gap_label = st.selectbox("انتخاب شکاف برای ایجاد برنامه توسعه", list(gap_options.keys()))
        selected_gap_id = gap_options[selected_gap_label]
        
        selected_gap = gaps_df[gaps_df['GapID'] == selected_gap_id].iloc[0]
        
        # نمایش اطلاعات شکاف انتخاب شده
        st.write("### اطلاعات شکاف انتخاب شده:")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**کارمند:** {selected_gap['EmployeeID']}")
            st.write(f"**شکاف:** {selected_gap['GapName']}")
            st.write(f"**نوع:** {selected_gap['GapType']}")
            st.write(f"**فوریت:** {selected_gap['Urgency']}")
        
        with col2:
            st.write(f"**سطح فعلی:** {selected_gap['CurrentLevel']}")
            st.write(f"**سطح مورد نیاز:** {selected_gap['RequiredLevel']}")
            st.write(f"**اندازه شکاف:** {selected_gap['GapSize']}")
            st.write(f"**وضعیت:** {selected_gap['Status']}")
        
        # فرم ایجاد برنامه توسعه
        with st.form("create_development_plan"):
            st.write("### ایجاد برنامه توسعه جدید")
            
            col1, col2 = st.columns(2)
            
            with col1:
                plan_name = st.text_input("نام برنامه *", placeholder="برنامه رفع شکاف طراحی معماری")
                plan_type = st.selectbox("نوع برنامه *", ["آموزش", "منتورینگ", "پروژه", "مطالعه", "کارگاه"])
                provider = st.text_input("ارائه‌دهنده", placeholder="آکادمی داخلی")
                
                # پیشنهاد دوره‌های مرتبط
                if not courses_df.empty and 'LinkedCompetency' in courses_df.columns:
                    related_courses = courses_df[courses_df['LinkedCompetency'].str.contains(selected_gap['GapName'], na=False)]
                    if not related_courses.empty:
                        st.write("**🎓 دوره‌های پیشنهادی:**")
                        for _, course in related_courses.iterrows():
                            st.write(f"- {course['CourseName']} ({course['Provider']})")
                
                start_date = st.date_input("تاریخ شروع", value=datetime.now())
            
            with col2:
                end_date = st.date_input("تاریخ پایان", value=datetime.now() + timedelta(days=30))
                estimated_hours = st.number_input("تخمین ساعت", min_value=1, value=8)
                cost = st.number_input("هزینه (ریال)", min_value=0, value=0)
                owner = st.text_input("مالک برنامه", value=selected_gap['Owner'])
            
            target_outcome = st.text_area("هدف نهایی", 
                                        value=selected_gap['SuccessMetric'])
            evaluation_method = st.text_input("روش ارزیابی", 
                                           placeholder="آزمون عملی، ارائه، پروژه")
            
            submitted = st.form_submit_button("📋 ایجاد برنامه توسعه")
            
            if submitted:
                if plan_name:
                    development_df = tms.load_sheet('Development_Plans')
                    
                    new_plan = {
                        'PlanID': f"PLAN-{len(development_df) + 1:03d}",
                        'GapID': selected_gap_id,
                        'PlanName': plan_name,
                        'PlanType': plan_type,
                        'Provider': provider,
                        'StartDate': start_date.strftime('%Y-%m-%d'),
                        'EndDate': end_date.strftime('%Y-%m-%d'),
                        'EstimatedHours': estimated_hours,
                        'Cost': cost,
                        'Owner': owner,
                        'TargetOutcome': target_outcome,
                        'EvaluationMethod': evaluation_method,
                        'Progress': 0,
                        'Status': 'برنامه‌ریزی شده'
                    }
                    
                    if development_df.empty:
                        development_df = pd.DataFrame([new_plan])
                    else:
                        development_df = pd.concat([development_df, pd.DataFrame([new_plan])], ignore_index=True)
                    
                    if tms.save_sheet(development_df, 'Development_Plans'):
                        # به‌روزرسانی وضعیت شکاف
                        gaps_df.loc[gaps_df['GapID'] == selected_gap_id, 'Status'] = 'در دست اقدام'
                        tms.save_sheet(gaps_df, 'Gaps')
                        
                        st.success("✅ برنامه توسعه با موفقیت ایجاد شد!")
                        st.balloons()
                else:
                    st.error("❌ لطفاً نام برنامه را وارد کنید")
        
        # نمایش برنامه‌های توسعه مرتبط
        if not development_df.empty:
            st.write("### برنامه‌های توسعه مرتبط با این شکاف:")
            related_plans = development_df[development_df['GapID'] == selected_gap_id]
            
            if not related_plans.empty:
                for _, plan in related_plans.iterrows():
                    with st.expander(f"📋 {plan['PlanName']} - {plan['Status']}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**نوع:** {plan['PlanType']}")
                            st.write(f"**ارائه‌دهنده:** {plan['Provider']}")
                            st.write(f"**تاریخ شروع:** {plan['StartDate']}")
                        
                        with col2:
                            st.write(f"**تاریخ پایان:** {plan['EndDate']}")
                            st.write(f"**هزینه:** {plan['Cost']:,} ریال")
                            st.write(f"**ساعت تخمینی:** {plan['EstimatedHours']} ساعت")
                        
                        with col3:
                            st.write(f"**پیشرفت:** {plan['Progress']}%")
                            st.write(f"**روش ارزیابی:** {plan['EvaluationMethod']}")
                            st.write(f"**هدف:** {plan['TargetOutcome']}")
                        
                        st.progress(plan['Progress'] / 100)
                        
                        # دکمه به‌روزرسانی پیشرفت
                        if st.button(f"🔄 به‌روزرسانی پیشرفت {plan['PlanID']}"):
                            update_progress(plan['PlanID'])
            else:
                st.info("📝 هیچ برنامه توسعه‌ای برای این شکاف تعریف نشده است.")
    else:
        st.info("📝 ابتدا شکاف ایجاد کنید")

def update_progress(plan_id):
    """به‌روزرسانی پیشرفت برنامه توسعه"""
    development_df = tms.load_sheet('Development_Plans')
    
    if not development_df.empty:
        plan_index = development_df[development_df['PlanID'] == plan_id].index[0]
        
        new_progress = st.slider("درصد پیشرفت جدید", 0, 100, 
                               development_df.loc[plan_index, 'Progress'])
        new_status = st.selectbox("وضعیت جدید", 
                                ["برنامه‌ریزی شده", "در جریان", "تکمیل شده", "متوقف شده"],
                                index=["برنامه‌ریزی شده", "در جریان", "تکمیل شده", "متوقف شده"]
                                .index(development_df.loc[plan_index, 'Status']))
        
        if st.button("💾 ذخیره تغییرات"):
            development_df.loc[plan_index, 'Progress'] = new_progress
            development_df.loc[plan_index, 'Status'] = new_status
            
            if tms.save_sheet(development_df, 'Development_Plans'):
                st.success("✅ پیشرفت برنامه با موفقیت به‌روزرسانی شد!")
                st.rerun()

def development_plan_management():
    """مدیریت برنامه‌های توسعه"""
    st.markdown("## 📈 مدیریت برنامه‌های توسعه")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 برنامه‌ها", "📊 پیگیری پیشرفت", "📈 گزارش اثربخشی", "💰 تحلیل مالی"])
    
    with tab1:
        show_development_plans()
    
    with tab2:
        track_progress()
    
    with tab3:
        effectiveness_report()
    
    with tab4:
        financial_analysis()

def show_development_plans():
    """نمایش برنامه‌های توسعه"""
    development_df = tms.load_sheet('Development_Plans')
    gaps_df = tms.load_sheet('Gaps')
    employees_df = tms.load_sheet('Employees')
    
    if not development_df.empty:
        # ارتباط داده‌ها
        merged_df = development_df.merge(
            gaps_df[['GapID', 'EmployeeID', 'GapName', 'GapSize']],
            on='GapID', how='left'
        ).merge(
            employees_df[['EmployeeID', 'FullName', 'Unit']],
            on='EmployeeID', how='left'
        )
        
        # فیلترها
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            statuses = ['همه'] + list(development_df['Status'].unique()) if 'Status' in development_df.columns else ['همه']
            selected_status = st.selectbox("وضعیت برنامه", statuses)
        
        with col2:
            plan_types = ['همه'] + list(development_df['PlanType'].unique()) if 'PlanType' in development_df.columns else ['همه']
            selected_type = st.selectbox("نوع برنامه", plan_types)
        
        with col3:
            units = ['همه'] + list(merged_df['Unit'].unique()) if 'Unit' in merged_df.columns else ['همه']
            selected_unit = st.selectbox("واحد سازمانی", units)
        
        with col4:
            providers = ['همه'] + list(development_df['Provider'].unique()) if 'Provider' in development_df.columns else ['همه']
            selected_provider = st.selectbox("ارائه‌دهنده", providers)
        
        # اعمال فیلترها
        filtered_df = merged_df.copy()
        if selected_status != 'همه' and 'Status' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Status'] == selected_status]
        if selected_type != 'همه' and 'PlanType' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['PlanType'] == selected_type]
        if selected_unit != 'همه' and 'Unit' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Unit'] == selected_unit]
        if selected_provider != 'همه' and 'Provider' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['Provider'] == selected_provider]
        
        st.info(f"📊 نمایش {len(filtered_df)} برنامه از {len(development_df)} برنامه")
        
        # نمایش جدول
        display_columns = ['FullName', 'Unit', 'GapName', 'PlanName', 'PlanType', 
                          'StartDate', 'EndDate', 'Progress', 'Status', 'Cost']
        
        # حذف ستون‌هایی که وجود ندارند
        display_columns = [col for col in display_columns if col in filtered_df.columns]
        
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True
        )
        
        # آمار مالی
        if 'Cost' in filtered_df.columns:
            total_cost = filtered_df['Cost'].sum()
        else:
            total_cost = 0
            
        if 'Progress' in filtered_df.columns:
            avg_progress = filtered_df['Progress'].mean()
        else:
            avg_progress = 0
            
        if 'EstimatedHours' in filtered_df.columns:
            total_hours = filtered_df['EstimatedHours'].sum()
        else:
            total_hours = 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 مجموع هزینه‌ها", f"{total_cost:,} ریال")
        with col2:
            st.metric("📊 میانگین پیشرفت", f"{avg_progress:.1f}%")
        with col3:
            st.metric("⏰ مجموع ساعت‌ها", f"{total_hours} ساعت")
            
    else:
        st.info("📝 هنوز برنامه توسعه‌ای ثبت نشده است.")

def track_progress():
    """پیگیری پیشرفت برنامه‌های توسعه"""
    st.subheader("📊 پیگیری پیشرفت برنامه‌های توسعه")
    
    development_df = tms.load_sheet('Development_Plans')
    gaps_df = tms.load_sheet('Gaps')
    employees_df = tms.load_sheet('Employees')
    
    if not development_df.empty:
        # انتخاب برنامه برای به‌روزرسانی
        plan_options = {f"{row['PlanID']} - {row['PlanName']}": row['PlanID'] 
                       for _, row in development_df.iterrows()}
        
        selected_plan_label = st.selectbox("انتخاب برنامه توسعه برای به‌روزرسانی", list(plan_options.keys()))
        selected_plan_id = plan_options[selected_plan_label]
        
        selected_plan = development_df[development_df['PlanID'] == selected_plan_id].iloc[0]
        
        # اطلاعات برنامه
        st.write("### اطلاعات برنامه انتخاب شده:")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**نام برنامه:** {selected_plan['PlanName']}")
            st.write(f"**نوع:** {selected_plan['PlanType']}")
            st.write(f"**ارائه‌دهنده:** {selected_plan['Provider']}")
            st.write(f"**وضعیت فعلی:** {selected_plan['Status']}")
        
        with col2:
            st.write(f"**پیشرفت فعلی:** {selected_plan['Progress']}%")
            st.write(f"**تاریخ شروع:** {selected_plan['StartDate']}")
            st.write(f"**تاریخ پایان:** {selected_plan['EndDate']}")
            st.write(f"**هزینه:** {selected_plan['Cost']:,} ریال")
        
        # اطلاعات شکاف مرتبط
        if not gaps_df.empty and not employees_df.empty and 'GapID' in selected_plan:
            related_gap = gaps_df[gaps_df['GapID'] == selected_plan['GapID']].iloc[0]
            related_employee = employees_df[employees_df['EmployeeID'] == related_gap['EmployeeID']].iloc[0]
            
            st.write("### اطلاعات شکاف و کارمند مرتبط:")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**کارمند:** {related_employee['FullName']}")
                st.write(f"**شکاف:** {related_gap['GapName']}")
                st.write(f"**واحد:** {related_employee['Unit']}")
            
            with col2:
                st.write(f"**سطح فعلی:** {related_gap['CurrentLevel']}")
                st.write(f"**سطح مورد نیاز:** {related_gap['RequiredLevel']}")
                st.write(f"**اندازه شکاف:** {related_gap['GapSize']}")
        
        # به‌روزرسانی پیشرفت
        st.write("### به‌روزرسانی پیشرفت:")
        col1, col2 = st.columns(2)
        
        with col1:
            new_progress = st.slider("درصد پیشرفت جدید", 0, 100, selected_plan['Progress'])
            status_options = ["برنامه‌ریزی شده", "در جریان", "تکمیل شده", "متوقف شده"]
            if selected_plan['Status'] in status_options:
                status_index = status_options.index(selected_plan['Status'])
            else:
                status_index = 0
            new_status = st.selectbox("وضعیت جدید", status_options, index=status_index)
        
        with col2:
            notes = st.text_area("یادداشت‌ها (اختیاری)", placeholder="توضیحاتی درباره پیشرفت...")
            completion_date = st.date_input("تاریخ تکمیل (در صورت اتمام)", 
                                          value=datetime.now() if new_progress == 100 else None,
                                          disabled=new_progress != 100)
        
        if st.button("💾 به‌روزرسانی پیشرفت"):
            development_df.loc[development_df['PlanID'] == selected_plan_id, 'Progress'] = new_progress
            development_df.loc[development_df['PlanID'] == selected_plan_id, 'Status'] = new_status
            
            if new_progress == 100 and new_status == 'تکمیل شده':
                development_df.loc[development_df['PlanID'] == selected_plan_id, 'EndDate'] = completion_date.strftime('%Y-%m-%d')
                
                # به‌روزرسانی وضعیت شکاف مرتبط
                if 'GapID' in selected_plan and pd.notna(selected_plan['GapID']):
                    gaps_df = tms.load_sheet('Gaps')
                    gaps_df.loc[gaps_df['GapID'] == selected_plan['GapID'], 'Status'] = 'حل شده'
                    
                    # به‌روزرسانی سطح فعلی کارمند
                    gap_info = gaps_df[gaps_df['GapID'] == selected_plan['GapID']].iloc[0]
                    new_current_level = gap_info['RequiredLevel']  # پس از تکمیل برنامه، سطح فعلی برابر سطح مورد نیاز می‌شود
                    gaps_df.loc[gaps_df['GapID'] == selected_plan['GapID'], 'CurrentLevel'] = new_current_level
                    gaps_df.loc[gaps_df['GapID'] == selected_plan['GapID'], 'GapSize'] = 0
                    
                    tms.save_sheet(gaps_df, 'Gaps')
            
            if tms.save_sheet(development_df, 'Development_Plans'):
                st.success("✅ پیشرفت برنامه با موفقیت به‌روزرسانی شد!")
                st.rerun()
        
        # نمایش نمودار پیشرفت
        st.write("### نمودار پیشرفت برنامه‌ها:")
        
        if 'PlanName' in development_df.columns and 'Progress' in development_df.columns and 'Status' in development_df.columns:
            progress_data = development_df[['PlanName', 'Progress', 'Status']]
            fig_progress = px.bar(
                progress_data,
                x='PlanName',
                y='Progress',
                color='Status',
                title="پیشرفت برنامه‌های توسعه",
                color_discrete_map={
                    'برنامه‌ریزی شده': 'gray',
                    'در جریان': 'blue', 
                    'تکمیل شده': 'green',
                    'متوقف شده': 'red'
                }
            )
            st.plotly_chart(fig_progress, use_container_width=True)
        
    else:
        st.info("📝 برنامه‌ای برای پیگیری وجود ندارد")

def effectiveness_report():
    """گزارش اثربخشی برنامه‌های توسعه"""
    st.subheader("📈 گزارش اثربخشی برنامه‌های توسعه")
    
    development_df = tms.load_sheet('Development_Plans')
    gaps_df = tms.load_sheet('Gaps')
    employees_df = tms.load_sheet('Employees')
    
    if not development_df.empty:
        # محاسبه اثربخشی
        completed_plans = development_df[development_df['Status'] == 'تکمیل شده']
        total_plans = len(development_df)
        completion_rate = (len(completed_plans) / total_plans * 100) if total_plans > 0 else 0
        
        # کارت‌های اثربخشی
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📋 کل برنامه‌ها", total_plans)
        
        with col2:
            st.metric("✅ برنامه‌های تکمیل شده", len(completed_plans))
        
        with col3:
            st.metric("📊 نرخ تکمیل", f"{completion_rate:.1f}%")
        
        with col4:
            if 'Cost' in development_df.columns:
                total_investment = development_df['Cost'].sum()
            else:
                total_investment = 0
            st.metric("💰 سرمایه‌گذاری کل", f"{total_investment:,} ریال")
        
        # تحلیل هزینه-اثربخشی
        st.write("### تحلیل هزینه-اثربخشی")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # هزینه بر اساس نوع برنامه
            if 'PlanType' in development_df.columns and 'Cost' in development_df.columns:
                cost_by_type = development_df.groupby('PlanType')['Cost'].sum()
                if not cost_by_type.empty:
                    fig_cost_type = px.pie(
                        values=cost_by_type.values,
                        names=cost_by_type.index,
                        title="توزیع هزینه بر اساس نوع برنامه"
                    )
                    st.plotly_chart(fig_cost_type, use_container_width=True)
        
        with col2:
            # اثربخشی بر اساس نوع برنامه
            if 'PlanType' in development_df.columns and 'Progress' in development_df.columns:
                effectiveness_by_type = development_df.groupby('PlanType')['Progress'].mean()
                if not effectiveness_by_type.empty:
                    fig_effectiveness = px.bar(
                        x=effectiveness_by_type.values,
                        y=effectiveness_by_type.index,
                        title="میانگین پیشرفت بر اساس نوع برنامه",
                        orientation='h'
                    )
                    st.plotly_chart(fig_effectiveness, use_container_width=True)
        
        # ROI تحلیلی
        st.write("### بازگشت سرمایه (ROI) تحلیلی")
        
        if not completed_plans.empty and not gaps_df.empty:
            # محاسبه ROI ساده
            completed_with_gaps = completed_plans.merge(
                gaps_df[['GapID', 'GapSize', 'ImpactOnTeam', 'ImpactOnOrg']],
                on='GapID', how='left'
            )
            
            # امتیازدهی به تأثیرات
            impact_score = {
                'کم': 1,
                'متوسط': 2,
                'زیاد': 3
            }
            
            completed_with_gaps['TeamImpactScore'] = completed_with_gaps['ImpactOnTeam'].map(impact_score)
            completed_with_gaps['OrgImpactScore'] = completed_with_gaps['ImpactOnOrg'].map(impact_score)
            completed_with_gaps['TotalImpact'] = completed_with_gaps['TeamImpactScore'] + completed_with_gaps['OrgImpactScore']
            
            # ROI ساده
            if 'Cost' in completed_with_gaps.columns:
                completed_with_gaps['ROI'] = (completed_with_gaps['TotalImpact'] * 1000000) / completed_with_gaps['Cost']
                completed_with_gaps['ROI'] = completed_with_gaps['ROI'].replace([np.inf, -np.inf], 0)
            
                st.dataframe(
                    completed_with_gaps[['PlanName', 'PlanType', 'Cost', 'TotalImpact', 'ROI']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # نمودار ROI
                fig_roi = px.scatter(
                    completed_with_gaps,
                    x='Cost',
                    y='TotalImpact',
                    size='ROI',
                    color='PlanType',
                    title="تحلیل ROI برنامه‌های توسعه",
                    size_max=40
                )
                st.plotly_chart(fig_roi, use_container_width=True)
        else:
            st.info("📊 برای محاسبه ROI نیاز به برنامه‌های تکمیل شده و داده‌های شکاف است")
    
    else:
        st.info("📈 داده‌ای برای گزارش‌گیری وجود ندارد")

def financial_analysis():
    """تحلیل مالی برنامه‌های توسعه"""
    st.subheader("💰 تحلیل مالی برنامه‌های توسعه")
    
    development_df = tms.load_sheet('Development_Plans')
    gaps_df = tms.load_sheet('Gaps')
    
    if not development_df.empty:
        # تحلیل هزینه‌ها
        col1, col2 = st.columns(2)
        
        with col1:
            # توزیع هزینه‌ها بر اساس وضعیت
            if 'Status' in development_df.columns and 'Cost' in development_df.columns:
                cost_by_status = development_df.groupby('Status')['Cost'].sum()
                if not cost_by_status.empty:
                    fig_cost_status = px.pie(
                        values=cost_by_status.values,
                        names=cost_by_status.index,
                        title="توزیع هزینه‌ها بر اساس وضعیت برنامه"
                    )
                    st.plotly_chart(fig_cost_status, use_container_width=True)
        
        with col2:
            # هزینه‌های ماهانه
            if 'StartDate' in development_df.columns and 'Cost' in development_df.columns:
                development_df['StartDate'] = pd.to_datetime(development_df['StartDate'])
                monthly_costs = development_df.groupby(development_df['StartDate'].dt.to_period('M'))['Cost'].sum()
                monthly_costs.index = monthly_costs.index.astype(str)
                
                fig_monthly = px.line(
                    x=monthly_costs.index,
                    y=monthly_costs.values,
                    title="هزینه‌های ماهانه برنامه‌های توسعه",
                    labels={'x': 'ماه', 'y': 'هزینه (ریال)'}
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
        
        # تحلیل بازگشت سرمایه
        st.write("### 📊 تحلیل بازگشت سرمایه (ROI)")
        
        if not gaps_df.empty:
            # محاسبه ROI پیشرفته
            development_with_gaps = development_df.merge(
                gaps_df[['GapID', 'GapSize', 'ImpactOnTeam', 'ImpactOnOrg', 'Urgency']],
                on='GapID', how='left'
            )
            
            # سیستم امتیازدهی پیشرفته
            urgency_multiplier = {
                'کم': 1,
                'متوسط': 1.5,
                'زیاد': 2
            }
            
            impact_score = {
                'کم': 1,
                'متوسط': 2,
                'زیاد': 3
            }
            
            if 'Cost' in development_with_gaps.columns:
                development_with_gaps['ROI_Score'] = (
                    development_with_gaps['GapSize'] * 
                    development_with_gaps['ImpactOnTeam'].map(impact_score) * 
                    development_with_gaps['ImpactOnOrg'].map(impact_score) *
                    development_with_gaps['Urgency'].map(urgency_multiplier) *
                    1000000 / development_with_gaps['Cost']
                )
                
                development_with_gaps['ROI_Score'] = development_with_gaps['ROI_Score'].replace([np.inf, -np.inf], 0)
                
                # نمایش ROI
                st.dataframe(
                    development_with_gaps[['PlanName', 'PlanType', 'Cost', 'GapSize', 'ROI_Score']].sort_values('ROI_Score', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
                
                # نمودار ROI
                fig_roi_advanced = px.scatter(
                    development_with_gaps,
                    x='Cost',
                    y='ROI_Score',
                    size='GapSize',
                    color='PlanType',
                    title="تحلیل پیشرفته ROI",
                    hover_data=['PlanName']
                )
                st.plotly_chart(fig_roi_advanced, use_container_width=True)
        
        # پیش‌بینی هزینه‌های آینده
        st.write("### 🔮 پیش‌بینی هزینه‌های آینده")
        
        planned_plans = development_df[development_df['Status'] == 'برنامه‌ریزی شده']
        total_planned_cost = planned_plans['Cost'].sum() if not planned_plans.empty and 'Cost' in planned_plans.columns else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 هزینه‌های برنامه‌ریزی شده", f"{total_planned_cost:,} ریال")
        with col2:
            st.metric("📋 تعداد برنامه‌های آینده", len(planned_plans))
        with col3:
            avg_planned_cost = total_planned_cost / len(planned_plans) if len(planned_plans) > 0 else 0
            st.metric("💵 میانگین هزینه برنامه", f"{avg_planned_cost:,.0f} ریال")
    
    else:
        st.info("💰 داده‌ای برای تحلیل مالی وجود ندارد")

def data_management():
    """مدیریت داده‌ها"""
    st.markdown("## 🗃️ مدیریت داده‌ها و گزارش‌گیری")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📥 نمونه‌سازی", "📊 گزارش‌های جامع", "📤 خروجی‌گیری", "⚙️ تنظیمات سیستم"])
    
    with tab1:
        st.subheader("ایجاد داده‌های نمونه")
        st.write("با کلیک روی دکمه زیر، داده‌های نمونه کامل برای تست سیستم ایجاد می‌شود.")
        
        if st.button("🔄 ایجاد داده‌های نمونه کامل", use_container_width=True):
            tms.generate_complete_sample_data()
            st.rerun()
        
        st.write("---")
        st.write("### داده‌های نمونه شامل:")
        st.write("✅ ۳ کارمند با اطلاعات کامل")
        st.write("✅ ۴ شایستگی شغلی")
        st.write("✅ ۳ شکاف مهارتی")
        st.write("✅ ۳ برنامه توسعه")
        st.write("✅ ۴ دوره آموزشی")
        st.write("✅ ۴ شاخص عملکرد (KPI)")
    
    with tab2:
        show_comprehensive_reports()
    
    with tab3:
        export_data()
    
    with tab4:
        system_settings()

def show_comprehensive_reports():
    """گزارش‌های جامع"""
    st.subheader("📊 گزارش‌های جامع تحلیلی")
    
    # بارگذاری تمام داده‌ها
    employees_df = tms.load_sheet('Employees')
    gaps_df = tms.load_sheet('Gaps')
    development_df = tms.load_sheet('Development_Plans')
    kpi_df = tms.load_sheet('KPI')
    
    if not employees_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # گزارش تحلیلی کارکنان
            st.write("### 📈 تحلیل کارکنان")
            
            # توزیع مرحله شغلی
            if 'CareerStage' in employees_df.columns:
                stage_dist = employees_df['CareerStage'].value_counts()
                fig_stage = px.bar(
                    x=stage_dist.values,
                    y=stage_dist.index,
                    title="توزیع مراحل شغلی",
                    orientation='h'
                )
                st.plotly_chart(fig_stage, use_container_width=True)
            
            # تحلیل انگیزه
            if 'MotivationScore' in employees_df.columns and 'CareerStage' in employees_df.columns:
                motivation_analysis = employees_df.groupby('CareerStage')['MotivationScore'].mean()
                if not motivation_analysis.empty:
                    fig_motivation = px.line(
                        x=motivation_analysis.index,
                        y=motivation_analysis.values,
                        title="میانگین انگیزه بر اساس مرحله شغلی"
                    )
                    st.plotly_chart(fig_motivation, use_container_width=True)
        
        with col2:
            # گزارش شکاف‌ها و توسعه
            st.write("### 🎯 تحلیل شکاف‌ها و توسعه")
            
            if not gaps_df.empty and not development_df.empty:
                # اثربخشی برنامه‌های توسعه
                gap_closure_rate = len(gaps_df[gaps_df['Status'] == 'حل شده']) / len(gaps_df) * 100
                
                fig_closure = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=gap_closure_rate,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "نرخ رفع شکاف‌ها"},
                    gauge={'axis': {'range': [None, 100]},
                          'bar': {'color': "darkblue"},
                          'steps': [{'range': [0, 50], 'color': "lightgray"},
                                   {'range': [50, 80], 'color': "gray"}],
                          'threshold': {'line': {'color': "red", 'width': 4},
                                      'thickness': 0.75, 'value': 90}}))
                
                st.plotly_chart(fig_closure, use_container_width=True)
            
            # تحلیل هزینه-فایده
            if not development_df.empty and 'PlanType' in development_df.columns and 'Cost' in development_df.columns and 'Progress' in development_df.columns:
                cost_effectiveness = development_df.groupby('PlanType').agg({
                    'Cost': 'sum',
                    'Progress': 'mean'
                }).reset_index()
                
                if not cost_effectiveness.empty:
                    fig_cost_effect = px.scatter(
                        cost_effectiveness,
                        x='Cost',
                        y='Progress',
                        size='Cost',
                        color='PlanType',
                        title="تحلیل هزینه-اثربخشی برنامه‌ها"
                    )
                    st.plotly_chart(fig_cost_effect, use_container_width=True)
        
        # گزارش عملکرد واحدها
        st.write("### 🏢 گزارش عملکرد واحدهای سازمانی")
        
        if not employees_df.empty and not gaps_df.empty and 'Unit' in employees_df.columns:
            unit_analysis = gaps_df.merge(
                employees_df[['EmployeeID', 'Unit']],
                on='EmployeeID', how='left'
            )
            
            if not unit_analysis.empty and 'Unit' in unit_analysis.columns:
                unit_performance = unit_analysis.groupby('Unit').agg({
                    'GapID': 'count',
                    'GapSize': 'mean',
                    'CostEstimate': 'sum'
                }).reset_index()
                
                fig_unit_perf = px.bar(
                    unit_performance,
                    x='Unit',
                    y='GapID',
                    color='GapSize',
                    title="تعداد و میانگین شکاف‌ها به تفکیک واحد",
                    hover_data=['CostEstimate']
                )
                st.plotly_chart(fig_unit_perf, use_container_width=True)
    
    else:
        st.info("📊 داده‌ای برای گزارش‌گیری وجود ندارد")

def export_data():
    """خروجی‌گیری داده‌ها"""
    st.subheader("📤 خروجی‌گیری داده‌ها")
    
    sheets = {
        'کارکنان': 'Employees',
        'ساختار سازمانی': 'Organization',
        'شایستگی‌ها': 'Competencies',
        'شکاف‌ها': 'Gaps',
        'برنامه‌های توسعه': 'Development_Plans',
        'دوره‌های آموزشی': 'Training_Courses',
        'شاخص‌های عملکرد': 'KPI'
    }
    
    selected_sheet = st.selectbox("انتخاب داده برای خروجی", list(sheets.keys()))
    
    df = tms.load_sheet(sheets[selected_sheet])
    
    if not df.empty:
        st.info(f"📊 تعداد رکوردهای {selected_sheet}: {len(df)}")
        
        # نمایش پیش‌نمایش
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # خروجی Excel
            try:
                excel_buffer = pd.ExcelWriter(f"{selected_sheet}_export.xlsx", engine='openpyxl')
                df.to_excel(excel_buffer, index=False)
                excel_buffer.close()
                
                with open(f"{selected_sheet}_export.xlsx", "rb") as file:
                    st.download_button(
                        label="📥 دانلود Excel",
                        data=file,
                        file_name=f"{selected_sheet}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.ms-excel"
                    )
            except Exception as e:
                st.error(f"خطا در ایجاد فایل Excel: {e}")
        
        with col2:
            # خروجی CSV
            csv_data = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 دانلود CSV",
                data=csv_data,
                file_name=f"{selected_sheet}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # خروجی کلی
        st.write("### خروجی کلی سیستم")
        if st.button("📦 خروجی کامل سیستم در یک فایل Excel"):
            try:
                all_data = {}
                for sheet_name in sheets.values():
                    all_data[sheet_name] = tms.load_sheet(sheet_name)
                
                output_file = f"complete_talent_system_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                
                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                    for sheet_name, sheet_data in all_data.items():
                        if not sheet_data.empty:
                            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
                
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="📥 دانلود فایل کامل سیستم",
                        data=file,
                        file_name=output_file,
                        mime="application/vnd.ms-excel"
                    )
            except Exception as e:
                st.error(f"خطا در ایجاد خروجی: {e}")
    
    else:
        st.info("📝 داده‌ای برای خروجی‌گیری وجود ندارد")

def system_settings():
    """تنظیمات سیستم"""
    st.subheader("⚙️ تنظیمات سیستم")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### اطلاعات سیستم")
        st.write(f"**تاریخ ایجاد:** {datetime.now().strftime('%Y/%m/%d %H:%M')}")
        st.write(f"**ورژن:** ۴.۰ - سیستم کامل")
        st.write(f"**تعداد جداول:** ۸")
        st.write(f"**فایل داده:** {DATA_FILE}")
        st.write(f"**تعداد ماژول‌ها:** ۵")
        
        # آمار سیستم
        employees_df = tms.load_sheet('Employees')
        gaps_df = tms.load_sheet('Gaps')
        development_df = tms.load_sheet('Development_Plans')
        
        st.write("### آمار سیستم")
        st.write(f"**کارکنان:** {len(employees_df) if not employees_df.empty else 0}")
        st.write(f"**شکاف‌ها:** {len(gaps_df) if not gaps_df.empty else 0}")
        st.write(f"**برنامه‌های توسعه:** {len(development_df) if not development_df.empty else 0}")
    
    with col2:
        st.write("### اقدامات سیستم")
        
        if st.button("🔍 بررسی سلامت داده‌ها", use_container_width=True):
            check_data_health()
        
        if st.button("🧹 بازنشانی سیستم", use_container_width=True):
            if st.checkbox("آیا مطمئن هستید؟ تمام داده‌ها پاک خواهند شد!"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                st.success("✅ سیستم بازنشانی شد!")
                st.rerun()
        
        if st.button("📋 لاگ سیستم", use_container_width=True):
            show_system_log()
        
        if st.button("🔄 بارگذاری مجدد داده‌ها", use_container_width=True):
            st.rerun()

def check_data_health():
    """بررسی سلامت داده‌ها"""
    st.write("### 🔍 گزارش سلامت داده‌ها")
    
    sheets = ['Employees', 'Competencies', 'Gaps', 'Development_Plans', 'KPI']
    
    health_status = []
    
    for sheet in sheets:
        df = tms.load_sheet(sheet)
        
        if df.empty:
            health_status.append({'شیت': sheet, 'وضعیت': '❌ خالی', 'رکوردها': 0, 'داده‌های مفقود': 0})
        else:
            null_count = df.isnull().sum().sum()
            total_cells = df.size
            null_percentage = (null_count / total_cells) * 100
            
            status = "✅ سالم" if null_percentage < 10 else "⚠️ نیاز به توجه" if null_percentage < 30 else "❌ مشکل‌دار"
            
            health_status.append({
                'شیت': sheet, 
                'وضعیت': status, 
                'رکوردها': len(df),
                'داده‌های مفقود': null_count
            })
    
    health_df = pd.DataFrame(health_status)
    st.dataframe(health_df, use_container_width=True, hide_index=True)
    
    # خلاصه وضعیت
    healthy_sheets = len([s for s in health_status if '✅' in s['وضعیت']])
    total_sheets = len(health_status)
    
    st.metric("📊 وضعیت کلی سیستم", f"{healthy_sheets}/{total_sheets} شیت سالم")

def show_system_log():
    """نمایش لاگ سیستم"""
    st.write("### 📋 لاگ سیستم")
    
    log_entries = [
        f"{datetime.now().strftime('%Y/%m/%d %H:%M')} - سیستم راه‌اندازی شد",
        f"{datetime.now().strftime('%Y/%m/%d %H:%M')} - ماژول شکاف‌ها اضافه شد",
        f"{datetime.now().strftime('%Y/%m/%d %H:%M')} - گزارش‌های پیشرفته فعال شد",
        f"{datetime.now().strftime('%Y/%m/%d %H:%M')} - سیستم کامل شد",
        f"{datetime.now().strftime('%Y/%m/%d %H:%M')} - تحلیل مالی اضافه شد"
    ]
    
    for log in log_entries:
        st.write(f"`{log}`")

def main():
    """تابع اصلی"""
    
    # منوی ناوبری
    st.sidebar.markdown("## 🧭 منوی ناوبری")
    
    menu_options = {
        "📊 داشبورد جامع": show_comprehensive_dashboard,
        "👥 مدیریت کارکنان": employee_management,
        "🎯 مدیریت شکاف‌ها": gap_management,
        "📈 برنامه‌های توسعه": development_plan_management,
        "🗃️ گزارش‌گیری پیشرفته": data_management
    }
    
    selected_menu = st.sidebar.radio("انتخاب بخش:", list(menu_options.keys()))
    
    # اجرای تابع مربوطه
    menu_options[selected_menu]()
    
    # اطلاعات پایین صفحه
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**آخرین به‌روزرسانی:** {datetime.now().strftime('%Y/%m/%d %H:%M')}")
    st.sidebar.markdown("**ورژن:** ۴.۰ - سیستم کامل")
    st.sidebar.markdown("**تعداد جداول:** ۸")
    st.sidebar.markdown("**وضعیت:** 🟢 فعال")

if __name__ == "__main__":
    main()
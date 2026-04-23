import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        /* Import Google Fonts (Inter) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Global Font */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Hide Streamlit components */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* KPI Cards / Metrics */
        [data-testid="stMetric"] {
            background-color: #1E293B; /* Slate 800 */
            border-radius: 12px;
            padding: 16px 20px;
            border-top: 4px solid #334155;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        /* Von Restorff Effect: Destacar KPI 2 (Itens Críticos) */
        div[data-testid="column"]:nth-of-type(2) [data-testid="stMetric"] {
            background-color: #E3001B !important;
            border-top: none;
            box-shadow: 0 10px 15px -3px rgba(227, 0, 27, 0.3);
        }
        div[data-testid="column"]:nth-of-type(2) [data-testid="stMetricLabel"] {
            color: #FFB3B8 !important;
        }
        div[data-testid="column"]:nth-of-type(2) [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem !important;
            color: #94A3B8 !important; /* Slate 400 */
            font-weight: 500 !important;
            margin-bottom: 4px;
        }
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #F8FAFC !important; /* Slate 50 */
        }
        [data-testid="stMetricDelta"] {
            font-size: 0.85rem !important;
        }

        /* Buttons Thumb Zone optimization (Minimum 48px) */
        .stButton > button {
            height: 48px !important;
            min-height: 48px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: background-color 0.2s ease, transform 0.1s ease !important;
        }
        /* Primary button specifically */
        .stButton > button[kind="primary"] {
            background-color: #E3001B !important;
            color: #FFFFFF !important;
            border: none !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #C00015 !important;
            transform: scale(0.98);
        }

        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.95) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid #334155;
        }

        /* Input fields and Selectboxes */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            min-height: 48px !important;
            border-radius: 8px !important;
        }

        /* Checkbox padding for touch */
        .stCheckbox {
            padding-top: 8px;
            padding-bottom: 8px;
        }
        
        /* Expander headers */
        .streamlit-expanderHeader {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
        }
        </style>
    """, unsafe_allow_html=True)

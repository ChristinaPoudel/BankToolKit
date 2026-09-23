import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# BANKDATA TOOLKIT: local Streamlit GUI for cleaning, analysis and visual dashboards.
st.set_page_config(page_title='BANKDATA TOOLKIT', page_icon='🏦', layout='wide')
st.title('🏦 BANKDATA TOOLKIT')
st.caption('Upload • Preview • Clean • Analyze • Visualize • Export')

if 'data' not in st.session_state:
    st.session_state.data = None

with st.sidebar:
    st.header('📁 Dataset')
    uploaded = st.file_uploader('Upload CSV or Excel', type=['csv', 'xlsx'])
    st.caption('Your file is processed in this running app session.')

if uploaded is not None:
    try:
        st.session_state.data = (pd.read_csv(uploaded) if uploaded.name.lower().endswith('.csv')
                                 else pd.read_excel(uploaded, engine='openpyxl'))
        st.sidebar.success('Dataset loaded')
    except Exception as exc:
        st.error(f'Unable to load file: {exc}')

if st.session_state.data is None:
    st.info('⬅ Upload a CSV/XLSX file from the sidebar. You can try sample_bank_data.csv included with the project.')
    st.stop()

df = st.session_state.data.copy()
numeric = df.select_dtypes(include='number').columns.tolist()
categorical = df.select_dtypes(include=['object', 'string', 'category']).columns.tolist()

# Top-level tabs make it easy to move between the raw preview, cleaner, analyzer and plots.
tab1, tab2, tab3, tab4 = st.tabs(['👁 Preview', '🧹 Cleaner', '💰 Expense Analyzer', '📊 Plot Dashboard'])

with tab1:
    st.subheader('Dataset Preview')
    a,b,c = st.columns(3)
    a.metric('Rows', f'{len(df):,}')
    b.metric('Columns', len(df.columns))
    c.metric('Missing cells', f'{int(df.isna().sum().sum()):,}')
    st.dataframe(df.head(200), use_container_width=True, height=430)

with tab2:
    st.subheader('Data Cleaner')
    c1,c2,c3 = st.columns(3)
    duplicates = c1.checkbox('Remove duplicates', True)
    empty = c2.checkbox('Remove empty rows', True)
    trim = c3.checkbox('Trim text spaces', True)
    if st.button('Clean Data', type='primary'):
        before = len(df)
        if duplicates: df = df.drop_duplicates()
        if empty: df = df.dropna(how='all')
        if trim:
            for col in df.select_dtypes(include=['object','string']).columns:
                df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
        st.session_state.data = df
        st.success(f'Cleaning finished. {before-len(df)} row(s) removed.')
    st.dataframe(st.session_state.data.head(200), use_container_width=True)

with tab3:
    st.subheader('Expense Analyzer')
    if not numeric:
        st.warning('A numeric column is required for expense analysis.')
    else:
        amount = st.selectbox('Amount column', numeric)
        group = st.selectbox('Group by', ['(None)'] + categorical)
        values = pd.to_numeric(df[amount], errors='coerce').dropna()
        a,b,c,d = st.columns(4)
        a.metric('Total', f'{values.sum():,.2f}')
        b.metric('Average', f'{values.mean():,.2f}')
        c.metric('Maximum', f'{values.max():,.2f}')
        d.metric('Records', f'{values.count():,}')
        if group != '(None)':
            summary = df.groupby(group, dropna=False)[amount].sum(min_count=1).sort_values(ascending=False).head(15)
            st.dataframe(summary.rename('Total').to_frame(), use_container_width=True)

with tab4:
    st.subheader('📊 Visual Plot Dashboard')
    st.caption('Choose columns and instantly view multiple plots in one dashboard.')
    if not numeric:
        st.warning('The dashboard needs at least one numeric column.')
    else:
        left, right = st.columns(2)
        metric = left.selectbox('Numeric column', numeric, key='dash_metric')
        category = right.selectbox('Category column', ['(None)'] + categorical, key='dash_category')

        # Four plots are arranged as a 2x2 visual dashboard for quick comparison.
        p1,p2 = st.columns(2)
        p3,p4 = st.columns(2)
        vals = pd.to_numeric(df[metric], errors='coerce').dropna()

        with p1:
            st.markdown('#### Histogram')
            fig, ax = plt.subplots(figsize=(7,4)); ax.hist(vals, bins=20, edgecolor='black')
            ax.set_xlabel(metric); ax.set_ylabel('Frequency'); ax.set_title(f'Distribution of {metric}')
            st.pyplot(fig, use_container_width=True); plt.close(fig)

        with p2:
            st.markdown('#### Box Plot')
            fig, ax = plt.subplots(figsize=(7,4)); ax.boxplot(vals.dropna(), vert=True)
            ax.set_ylabel(metric); ax.set_title(f'Box Plot of {metric}')
            st.pyplot(fig, use_container_width=True); plt.close(fig)

        with p3:
            st.markdown('#### Trend / Row Plot')
            fig, ax = plt.subplots(figsize=(7,4)); ax.plot(vals.reset_index(drop=True))
            ax.set_xlabel('Row'); ax.set_ylabel(metric); ax.set_title(f'{metric} Trend')
            st.pyplot(fig, use_container_width=True); plt.close(fig)

        with p4:
            st.markdown('#### Category Bar Chart')
            if category == '(None)':
                st.info('Select a category column above to display this chart.')
            else:
                grouped = df.groupby(category, dropna=False)[metric].sum(min_count=1).sort_values(ascending=False).head(12)
                fig, ax = plt.subplots(figsize=(7,4)); grouped.plot(kind='bar', ax=ax)
                ax.set_xlabel(category); ax.set_ylabel(metric); ax.set_title(f'{metric} by {category}')
                plt.xticks(rotation=40, ha='right'); plt.tight_layout()
                st.pyplot(fig, use_container_width=True); plt.close(fig)

        st.markdown('#### Numeric Correlation Heatmap')
        if len(numeric) >= 2:
            corr = df[numeric].corr(numeric_only=True)
            fig, ax = plt.subplots(figsize=(9,5)); im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
            ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=45, ha='right')
            ax.set_yticks(range(len(corr.columns)), corr.columns)
            fig.colorbar(im, ax=ax, label='Correlation'); ax.set_title('Correlation between numeric columns')
            plt.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)
        else:
            st.info('At least two numeric columns are required for the correlation heatmap.')

st.divider()
st.subheader('📥 Export Processed Dataset')
out = st.session_state.data.to_csv(index=False).encode('utf-8')
st.download_button('Export Report (CSV)', out, 'bankdata_cleaned_report.csv', 'text/csv')

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
from datetime import datetime, timezone

st.set_page_config(page_title='Fashion Market Intelligence', page_icon='👗', layout='wide')
st.title('Fashion Market Intelligence')
st.caption('150 curated ticker candidates across global apparel, luxury, footwear, accessories and fashion retail | Data: Yahoo Finance via yfinance')
st.info('The 150 entries are candidate listings, not 150 guaranteed live financial records. Some symbols may be stale or have missing data. Financial metrics belong to publicly traded parent companies, not individual private labels. For example, Balenciaga and Gucci are brands of Kering; Dior and Louis Vuitton are part of LVMH. Missing values are not estimated.')

# Curated universe of publicly listed companies and their brands. This is intentionally
# a focused fashion universe, not an invented 100-company sample.
COMPANIES = [('KER.PA', 'Kering', 'Luxury', 'France', 'Balenciaga, Gucci, Saint Laurent, Bottega Veneta'), ('MC.PA', 'LVMH', 'Luxury', 'France', 'Louis Vuitton, Dior, Fendi, Loewe, Celine'), ('RMS.PA', 'Hermes', 'Luxury', 'France', 'Hermes'), ('BRBY.L', 'Burberry', 'Luxury', 'UK', 'Burberry'), ('MONC.MI', 'Moncler', 'Luxury', 'Italy', 'Moncler, Stone Island'), ('ZGN', 'Ermenegildo Zegna', 'Luxury', 'Italy', 'Zegna, Thom Browne, Tom Ford Fashion'), ('BC.MI', 'Brunello Cucinelli', 'Luxury', 'Italy', 'Brunello Cucinelli'), ('1913.HK', 'Prada', 'Luxury', 'Italy', 'Prada, Miu Miu'), ('CPRI', 'Capri Holdings', 'Luxury', 'USA', 'Michael Kors, Jimmy Choo'), ('TPR', 'Tapestry', 'Luxury', 'USA', 'Coach, Kate Spade'), ('RL', 'Ralph Lauren', 'Premium apparel', 'USA', 'Ralph Lauren'), ('PVH', 'PVH', 'Premium apparel', 'USA', 'Calvin Klein, Tommy Hilfiger'), ('VFC', 'VF Corporation', 'Apparel & outdoor', 'USA', 'The North Face, Vans, Timberland'), ('HUG.DE', 'Hugo Boss', 'Premium apparel', 'Germany', 'Boss, Hugo'), ('ADS.DE', 'Adidas', 'Sportswear', 'Germany', 'Adidas'), ('PUM.DE', 'Puma', 'Sportswear', 'Germany', 'Puma'), ('NKE', 'Nike', 'Sportswear', 'USA', 'Nike, Jordan'), ('UAA', 'Under Armour', 'Sportswear', 'USA', 'Under Armour'), ('LULU', 'Lululemon', 'Sportswear', 'Canada', 'Lululemon'), ('ONON', 'On Holding', 'Sportswear', 'Switzerland', 'On'), ('DECK', 'Deckers Outdoor', 'Footwear', 'USA', 'Hoka, UGG'), ('CROX', 'Crocs', 'Footwear', 'USA', 'Crocs, HEYDUDE'), ('SKX', 'Skechers', 'Footwear', 'USA', 'Skechers'), ('BIRK', 'Birkenstock', 'Footwear', 'Germany', 'Birkenstock'), ('WWW', 'Wolverine Worldwide', 'Footwear', 'USA', 'Merrell, Saucony, Wolverine'), ('SHOO', 'Steven Madden', 'Footwear', 'USA', 'Steve Madden'), ('CAL', 'Caleres', 'Footwear', 'USA', 'Sam Edelman, Famous Footwear'), ('GCO', 'Genesco', 'Footwear', 'USA', 'Journeys, Johnston & Murphy'), ('COLM', 'Columbia Sportswear', 'Apparel & outdoor', 'USA', 'Columbia, SOREL, prAna'), ('GOOS', 'Canada Goose', 'Apparel & outdoor', 'Canada', 'Canada Goose'), ('FIGS', 'FIGS', 'Specialty apparel', 'USA', 'FIGS'), ('WRBY', 'Warby Parker', 'Accessories', 'USA', 'Warby Parker'), ('OXM', 'Oxford Industries', 'Premium apparel', 'USA', 'Tommy Bahama, Lilly Pulitzer'), ('LEVI', 'Levi Strauss', 'Denim & casual', 'USA', 'Levis'), ('KTB', 'Kontoor Brands', 'Denim & casual', 'USA', 'Wrangler, Lee'), ('GIII', 'G-III Apparel', 'Apparel & outdoor', 'USA', 'DKNY, Karl Lagerfeld'), ('GAP', 'Gap', 'Fashion retail', 'USA', 'Gap, Old Navy, Banana Republic, Athleta'), ('ANF', 'Abercrombie & Fitch', 'Fashion retail', 'USA', 'Abercrombie, Hollister'), ('AEO', 'American Eagle', 'Fashion retail', 'USA', 'American Eagle, Aerie'), ('URBN', 'Urban Outfitters', 'Fashion retail', 'USA', 'Urban Outfitters, Anthropologie, Free People'), ('BKE', 'Buckle', 'Fashion retail', 'USA', 'Buckle'), ('ITX.MC', 'Inditex', 'Fashion retail', 'Spain', 'Zara, Massimo Dutti, Bershka, Pull&Bear'), ('HM-B.ST', 'H&M', 'Fashion retail', 'Sweden', 'H&M, COS, ARKET'), ('FRAS.L', 'Frasers Group', 'Fashion retail', 'UK', 'Sports Direct, Flannels'), ('NXT.L', 'Next', 'Fashion retail', 'UK', 'Next'), ('JD.L', 'JD Sports', 'Fashion retail', 'UK', 'JD Sports'), ('9983.T', 'Fast Retailing', 'Fashion retail', 'Japan', 'Uniqlo, GU'), ('7936.T', 'Asics', 'Sportswear', 'Japan', 'Asics'), ('VIPS', 'Vipshop', 'Fashion retail', 'China', 'Multi-brand retailer'), ('BURL', 'Burlington Stores', 'Fashion retail', 'USA', 'Multi-brand retailer'), ('ROST', 'Ross Stores', 'Fashion retail', 'USA', 'Multi-brand retailer'), ('TJX', 'TJX Companies', 'Fashion retail', 'USA', 'TJ Maxx, Marshalls'), ('M', 'Macys', 'Fashion retail', 'USA', 'Macys, Bloomingdales'), ('KSS', 'Kohls', 'Fashion retail', 'USA', 'Kohls'), ('DDS', 'Dillards', 'Fashion retail', 'USA', 'Dillards'), ('FL', 'Foot Locker', 'Footwear', 'USA', 'Foot Locker'), ('DBI', 'Designer Brands', 'Footwear', 'USA', 'DSW'), ('BOOT', 'Boot Barn', 'Footwear', 'USA', 'Boot Barn'), ('SCVL', 'Shoe Carnival', 'Footwear', 'USA', 'Shoe Carnival'), ('ZUMZ', 'Zumiez', 'Fashion retail', 'USA', 'Zumiez'), ('VSCO', 'Victoria’s Secret', 'Specialty apparel', 'USA', 'Victorias Secret, PINK'), ('PLCE', 'Childrens Place', 'Specialty apparel', 'USA', 'The Childrens Place'), ('CTRN', 'Citi Trends', 'Fashion retail', 'USA', 'Citi Trends'), ('DLTH', 'Duluth Holdings', 'Specialty apparel', 'USA', 'Duluth Trading'), ('TLYS', 'Tillys', 'Fashion retail', 'USA', 'Tillys'), ('DTC', 'Solo Brands', 'Apparel & outdoor', 'USA', 'Chubbies'), ('AKA', 'a.k.a. Brands', 'Fashion retail', 'USA', 'Princess Polly, Culture Kings'), ('RVLV', 'Revolve', 'Fashion retail', 'USA', 'Revolve, FWRD'), ('REAL', 'The RealReal', 'Luxury resale', 'USA', 'Luxury resale marketplace'), ('SFIX', 'Stitch Fix', 'Fashion retail', 'USA', 'Stitch Fix'), ('RENT', 'Rent the Runway', 'Fashion retail', 'USA', 'Rent the Runway'), ('ASC.L', 'ASOS', 'Fashion retail', 'UK', 'ASOS'), ('BOO.L', 'Boohoo', 'Fashion retail', 'UK', 'Boohoo, PrettyLittleThing'), ('DOCS.L', 'Dr. Martens', 'Footwear', 'UK', 'Dr. Martens'), ('2020.HK', 'ANTA Sports', 'Sportswear', 'China', 'ANTA, FILA China'), ('2331.HK', 'Li Ning', 'Sportswear', 'China', 'Li Ning'), ('1368.HK', 'Xtep', 'Sportswear', 'China', 'Xtep'), ('3998.HK', 'Bosideng', 'Apparel & outdoor', 'China', 'Bosideng'), ('3813.HK', 'Pou Sheng', 'Footwear', 'China', 'Athletic footwear retail'), ('1234.HK', 'China Lilang', 'Premium apparel', 'China', 'Lilang'), ('3306.HK', 'JNBY Design', 'Premium apparel', 'China', 'JNBY'), ('6110.HK', 'Topsports', 'Footwear', 'China', 'Sports footwear retail'), ('600398.SS', 'HLA Group', 'Premium apparel', 'China', 'HLA'), ('002563.SZ', 'Semir', 'Denim & casual', 'China', 'Semir, Balabala'), ('002154.SZ', 'Baoxiniao', 'Premium apparel', 'China', 'Baoxiniao'), ('002029.SZ', 'Septwolves', 'Premium apparel', 'China', 'Septwolves'), ('002327.SZ', 'Fujian Fynex Textile', 'Apparel & outdoor', 'China', 'Textiles'), ('TRENT.NS', 'Trent', 'Fashion retail', 'India', 'Westside, Zudio'), ('ABFRL.NS', 'Aditya Birla Fashion', 'Fashion retail', 'India', 'Pantaloons, Louis Philippe'), ('ARVINDFASN.NS', 'Arvind Fashions', 'Premium apparel', 'India', 'Arrow, US Polo Assn India'), ('PAGEIND.NS', 'Page Industries', 'Specialty apparel', 'India', 'Jockey India'), ('VEDANTFASH.NS', 'Vedant Fashions', 'Specialty apparel', 'India', 'Manyavar'), ('RAYMOND.NS', 'Raymond', 'Premium apparel', 'India', 'Raymond'), ('KPRMILL.NS', 'KPR Mill', 'Apparel & outdoor', 'India', 'Textile manufacturing'), ('GOKEX.NS', 'Gokaldas Exports', 'Apparel & outdoor', 'India', 'Apparel manufacturing'), ('ZAL.DE', 'Zalando', 'Fashion retail', 'Germany', 'Zalando'), ('SFER.MI', 'Salvatore Ferragamo', 'Luxury', 'Italy', 'Ferragamo'), ('CFR.SW', 'Richemont', 'Luxury', 'Switzerland', 'Chloe, Alaia, Cartier'), ('UHR.SW', 'Swatch Group', 'Accessories', 'Switzerland', 'Swatch, Omega'), ('VTX.PA', 'Vente-Unique', 'Fashion retail', 'France', 'Online retail'), ('SMCP.PA', 'SMCP', 'Premium apparel', 'France', 'Sandro, Maje, Claudie Pierlot'), ('CDI.PA', 'Christian Dior SE', 'Luxury', 'France', 'Dior holding company'), ('EL.PA', 'EssilorLuxottica', 'Accessories', 'France', 'Ray-Ban, Oakley'), ('MKS.L', 'Marks & Spencer', 'Fashion retail', 'UK', 'M&S Clothing'), ('BME.L', 'B&M European Value Retail', 'Fashion retail', 'UK', 'Apparel assortment'), ('ABF.L', 'Associated British Foods', 'Fashion retail', 'UK', 'Primark'), ('SHOE.L', 'Shoe Zone', 'Footwear', 'UK', 'Shoe Zone'), ('BOOZT.ST', 'Boozt', 'Fashion retail', 'Sweden', 'Boozt'), ('RVRC.ST', 'RevolutionRace', 'Apparel & outdoor', 'Sweden', 'RevolutionRace'), ('NLY.ST', 'Nelly Group', 'Fashion retail', 'Sweden', 'Nelly'), ('BJORN-B.ST', 'Bjorn Borg', 'Premium apparel', 'Sweden', 'Bjorn Borg'), ('DOUG.DE', 'Douglas', 'Fashion retail', 'Germany', 'Beauty retail adjacent'), ('GFG.DE', 'Global Fashion Group', 'Fashion retail', 'Luxembourg', 'Dafiti, Zalora'), ('CEAB3.SA', 'C&A Modas', 'Fashion retail', 'Brazil', 'C&A'), ('LREN3.SA', 'Lojas Renner', 'Fashion retail', 'Brazil', 'Renner'), ('GUAR3.SA', 'Guararapes', 'Fashion retail', 'Brazil', 'Riachuelo'), ('AZZA3.SA', 'Azzas 2154', 'Footwear', 'Brazil', 'Arezzo, Schutz, Reserva'), ('ALPA4.SA', 'Alpargatas', 'Footwear', 'Brazil', 'Havaianas'), ('VULC3.SA', 'Vulcabras', 'Footwear', 'Brazil', 'Olympikus'), ('TFCO4.SA', 'Track & Field', 'Sportswear', 'Brazil', 'Track & Field'), ('LPP.WA', 'LPP', 'Fashion retail', 'Poland', 'Reserved, Cropp, Sinsay'), ('CCC.WA', 'CCC', 'Footwear', 'Poland', 'CCC, HalfPrice'), ('VRG.WA', 'VRG', 'Premium apparel', 'Poland', 'Vistula, Wólczanka'), ('MONN.WA', 'Monnari Trade', 'Fashion retail', 'Poland', 'Monnari'), ('ANS.WA', 'Answear.com', 'Fashion retail', 'Poland', 'Answear'), ('MAVI.IS', 'Mavi Giyim', 'Denim & casual', 'Turkey', 'Mavi'), ('VAKKO.IS', 'Vakko', 'Luxury', 'Turkey', 'Vakko'), ('DERIM.IS', 'Derimod', 'Footwear', 'Turkey', 'Derimod'), ('DESA.IS', 'Desa Deri', 'Accessories', 'Turkey', 'Desa'), ('KOTON.IS', 'Koton', 'Fashion retail', 'Turkey', 'Koton'), ('SUWEN.IS', 'Suwen Tekstil', 'Specialty apparel', 'Turkey', 'Suwen'), ('BOSSA.IS', 'Bossa', 'Denim & casual', 'Turkey', 'Denim manufacturing'), ('3092.T', 'ZOZO', 'Fashion retail', 'Japan', 'ZOZOTOWN'), ('7453.T', 'Ryohin Keikaku', 'Fashion retail', 'Japan', 'MUJI'), ('2685.T', 'Adastria', 'Fashion retail', 'Japan', 'GLOBAL WORK, niko and'), ('8227.T', 'Shimamura', 'Fashion retail', 'Japan', 'Shimamura'), ('8016.T', 'Onward Holdings', 'Premium apparel', 'Japan', '23KU, J.PRESS'), ('3591.T', 'Wacoal Holdings', 'Specialty apparel', 'Japan', 'Wacoal'), ('3608.T', 'TSI Holdings', 'Fashion retail', 'Japan', 'Nano Universe'), ('3612.T', 'World Co', 'Fashion retail', 'Japan', 'World'), ('7606.T', 'United Arrows', 'Fashion retail', 'Japan', 'United Arrows'), ('2670.T', 'ABC-Mart', 'Footwear', 'Japan', 'ABC-Mart'), ('8111.T', 'Goldwin', 'Apparel & outdoor', 'Japan', 'Goldwin'), ('8022.T', 'Mizuno', 'Sportswear', 'Japan', 'Mizuno'), ('8114.T', 'Descente', 'Sportswear', 'Japan', 'Descente'), ('8011.T', 'Sanyo Shokai', 'Premium apparel', 'Japan', 'Sanyo Shokai'), ('3611.T', 'Matsuoka', 'Apparel & outdoor', 'Japan', 'Apparel manufacturing'), ('3205.T', 'Daidoh', 'Premium apparel', 'Japan', 'New Yorker'), ('005390.KS', 'Shinsung Tongsang', 'Fashion retail', 'South Korea', 'TOPTEN10'), ('093050.KS', 'LF Corp', 'Premium apparel', 'South Korea', 'Hazzys, Daks')]
# Remove explicit non-fashion placeholders and obvious duplicated/unsupported proxies.
COMPANIES = [r for r in COMPANIES if r[2] != 'Other' and '(if available)' not in r[1]]
master = pd.DataFrame(COMPANIES, columns=['Ticker','Company','Segment','Country','Brands'])
master = master.drop_duplicates('Ticker')

METRICS = {
'Market Cap (B local)': ('marketCap', 1e9), 'Revenue (B local)': ('totalRevenue', 1e9),
'Revenue Growth (%)': ('revenueGrowth', 0.01), 'Gross Margin (%)': ('grossMargins', 0.01),
'Operating Margin (%)': ('operatingMargins', 0.01), 'Profit Margin (%)': ('profitMargins', 0.01),
'ROE (%)': ('returnOnEquity', 0.01), 'ROA (%)': ('returnOnAssets', 0.01),
'P/E Ratio': ('trailingPE', 1), 'Forward P/E': ('forwardPE', 1),
'Price/Book': ('priceToBook', 1), 'Price/Sales': ('priceToSalesTrailing12Months', 1),
'EV/EBITDA': ('enterpriseToEbitda', 1), 'Debt/Equity': ('debtToEquity', 1),
'Current Ratio': ('currentRatio', 1), 'Dividend Yield (%)': ('dividendYield', 0.01),
'Beta': ('beta', 1), '52-Week Change (%)': ('52WeekChange', 0.01),
'Free Cash Flow (B local)': ('freeCashflow', 1e9), 'Employees': ('fullTimeEmployees', 1),
}

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_one(ticker):
    try:
        info = yf.Ticker(ticker).info
        if not info or not (info.get('marketCap') or info.get('totalRevenue')):
            return None
        row = {'Ticker': ticker, 'Currency': info.get('currency', 'Unknown'),
               'Last refreshed (UTC)': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}
        for label, (key, divisor) in METRICS.items():
            v = info.get(key)
            row[label] = (float(v) / divisor) if isinstance(v, (int,float)) and np.isfinite(v) else np.nan
        return row
    except Exception:
        return None

st.sidebar.header('Universe')
segments = st.sidebar.multiselect('Fashion segments', sorted(master.Segment.unique()), default=sorted(master.Segment.unique()))
countries = st.sidebar.multiselect('Countries', sorted(master.Country.unique()), default=sorted(master.Country.unique()))
search = st.sidebar.text_input('Search company or brand', placeholder='Balenciaga, Prada, Crocs...')
universe = master[master.Segment.isin(segments) & master.Country.isin(countries)]
if search:
    universe = universe[universe[['Company','Brands','Ticker']].fillna('').apply(lambda c: c.str.contains(search, case=False, regex=False)).any(axis=1)]
st.sidebar.caption(f'{len(universe)} companies in selected universe; inactive/delisted tickers may have no current data.')
limit = st.sidebar.slider('Maximum companies to request', 5, max(5,len(master)), min(25,max(5,len(master))), 5)
st.sidebar.warning('Initial live data retrieval may take several minutes. Financial data can be delayed, incomplete, or subject to vendor limits.')
load = st.sidebar.button('Load / refresh selected companies', type='primary')
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if load:
    rows=[]
    progress=st.progress(0)
    selected=universe.head(limit)
    for i, ticker in enumerate(selected.Ticker):
        r=fetch_one(ticker)
        if r: rows.append(r)
        progress.progress((i+1)/len(selected))
    st.session_state.data = selected.merge(pd.DataFrame(rows), on='Ticker', how='inner') if rows else pd.DataFrame()
    progress.empty()

df=st.session_state.data.copy()
if df.empty:
    st.info('Choose your fashion segments and click **Load / refresh selected companies** to retrieve real public-company financial data.')
    st.dataframe(universe, hide_index=True, use_container_width=True)
    st.stop()

st.caption('Dollar-based metrics are shown in each company’s reporting currency (see Currency). Cross-currency dollar amounts are NOT directly comparable. Ratios and percentages are generally more comparable but may differ in accounting basis and reporting period.')
st.sidebar.header('Financial screening')
chosen = st.sidebar.multiselect('Choose financial sliders', list(METRICS), default=['Market Cap (B local)','Revenue Growth (%)','Gross Margin (%)','Operating Margin (%)','P/E Ratio','ROE (%)'])
filtered=df.copy()
for col in chosen:
    values=df[col].dropna()
    if values.empty:
        st.sidebar.caption(f'{col}: unavailable')
        continue
    lo,hi=float(values.min()),float(values.max())
    if lo == hi:
        st.sidebar.caption(f'{col}: only one available value ({lo:.2f})')
        continue
    a,b=st.sidebar.slider(col, min_value=lo, max_value=hi, value=(lo,hi), step=max((hi-lo)/1000,0.0001), format='%.3f', key='filter_'+col)
    filtered=filtered[filtered[col].between(a,b, inclusive='both')]

c1,c2,c3,c4=st.columns(4)
c1.metric('Loaded companies',len(df))
c2.metric('Matching companies',len(filtered))
c3.metric('Segments',filtered.Segment.nunique())
c4.metric('Countries',filtered.Country.nunique())

t1,t2,t3,t4=st.tabs(['Screener','Compare & visualize','Industry analysis','Data quality & export'])
with t1:
    st.subheader('Company screener')
    st.dataframe(filtered, use_container_width=True, hide_index=True)
with t2:
    if filtered.empty:
        st.warning('No companies match these filters.')
    else:
        choices=st.multiselect('Companies to compare', filtered.Ticker.tolist(), default=filtered.Ticker.head(8).tolist())
        x=st.selectbox('Horizontal metric',list(METRICS),index=list(METRICS).index('Revenue Growth (%)'))
        y=st.selectbox('Vertical metric',list(METRICS),index=list(METRICS).index('Operating Margin (%)'))
        plot=filtered[filtered.Ticker.isin(choices)].dropna(subset=[x,y])
        if not plot.empty:
            st.plotly_chart(px.scatter(plot,x=x,y=y,color='Segment',hover_name='Company',hover_data=['Ticker','Currency'],title=f'{y} vs {x}'),use_container_width=True)
        metric=st.selectbox('Ranking metric',list(METRICS),index=list(METRICS).index('ROE (%)'))
        ranks=filtered.dropna(subset=[metric]).sort_values(metric,ascending=False).head(20)
        if not ranks.empty:
            st.plotly_chart(px.bar(ranks,x='Company',y=metric,color='Segment',title=f'Top companies by {metric}'),use_container_width=True)
with t3:
    metric=st.selectbox('Metric for industry comparison',list(METRICS),index=list(METRICS).index('Profit Margin (%)'),key='industry_metric')
    if not filtered.empty:
        summary=filtered.groupby('Segment').agg(Companies=('Ticker','count'),Median=(metric,'median'),Mean=(metric,'mean')).reset_index()
        st.dataframe(summary,hide_index=True,use_container_width=True)
        st.plotly_chart(px.bar(summary,x='Segment',y='Median',title=f'Median {metric} by fashion segment'),use_container_width=True)
        st.caption('Industry results are based on companies with available data, not a representative sample of all fashion brands.')
with t4:
    st.subheader('Coverage and limitations')
    st.write(f'{len(master)} curated tickers; {len(df)} returned usable financial data. Unavailable or delisted securities are excluded from results.')
    coverage=pd.DataFrame({'Metric':list(METRICS),'Available observations':[int(df[m].notna().sum()) for m in METRICS]})
    st.dataframe(coverage,hide_index=True,use_container_width=True)
    st.download_button('Download screened results (CSV)',filtered.to_csv(index=False).encode('utf-8'),'fashion_screened.csv','text/csv')
    st.download_button('Download all loaded results (CSV)',df.to_csv(index=False).encode('utf-8'),'fashion_all_loaded.csv','text/csv')
    st.caption('Source: Yahoo Finance data via yfinance. Data may be missing, stale or inaccurate. Not investment advice.')

import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title='가천 도서관 좌석 안내 시연', page_icon='📚', layout='wide')
st.markdown('''<style>
.block-container {max-width: 1050px; padding-top: 1.5rem;}
div[data-testid="stMetric"] {background:#f2f6f4; padding:14px; border-radius:13px;}
.seat-legend {display:flex; gap:12px; flex-wrap:wrap; margin:10px 0; font-size:0.9rem;}
.dot {display:inline-block; width:13px; height:13px; border-radius:3px; margin-right:4px; vertical-align:middle;}
</style>''', unsafe_allow_html=True)

st.title('📚 가천 도서관 좌석 안내 서비스')
st.caption('공모전 시연용 시제품 · 모든 좌석 정보는 가상 데이터이며 실제 도서관 시스템과 연결되지 않음')

page1, page2, page3 = st.tabs(['종료 예정 좌석 현황', '좌석 배치도 시각화', '외출 복귀 알림 시연'])

with page1:
    st.subheader('중앙도서관 2층 열람실')
    st.markdown('**첨부한 화면 구성 예시**')
    st.image('reference.png', caption='제안서에 사용할 종료 예정 좌석 현황 예시')
    st.info('향후 실제 예약 종료 시각을 제공받으면 이 요약 화면을 자동 갱신하도록 개발할 수 있음')

# 여러 종료 예정 시각을 가정한 독립 시연용 데이터
# 종료 예정 시각은 현재 시각 기준으로 구성하므로 시연 중 값이 안정적으로 보임.
remaining = [5, 9, 12, 16, 22, 27, 32, 36, 41, 47, 52, 59, 75, 84, 95, 113, 126, 148, 173, 184, 205, 219, 235, 260, 283, 310, 345, 370, 398, 420, 460, 490, 515, 555, 590, 610]
seat_data = {i+1: remaining[i] for i in range(len(remaining))}

with page2:
    st.subheader('종료 예정 좌석 시각화')
    window = st.select_slider('종료 예정 좌석 확인 범위', options=[10, 30, 60], value=30, format_func=lambda x: f'{x}분 이내')
    n = sum(1 for t in remaining if t <= window)
    a,b,c = st.columns(3)
    a.metric('시연용 전체 좌석', f'{len(seat_data)}석')
    b.metric('현재 빈자리', '0석')
    c.metric(f'{window}분 내 종료 예정', f'{n}석')
    st.markdown('''<div class="seat-legend"><span><span class="dot" style="background:#2185c5"></span>이용 가능</span><span><span class="dot" style="background:#f4ad44"></span>선택 시간 내 종료 예정</span><span><span class="dot" style="background:#3c4856"></span>이용 중</span></div>''', unsafe_allow_html=True)
    st.caption('아래 좌석 번호와 종료 예정시간은 가상 데이터임. 주황색은 실제 공석을 보장하지 않음.')
    for start in range(1, len(seat_data)+1, 6):
        cols = st.columns(6)
        for j, col in enumerate(cols):
            seat_no = start + j
            if seat_no not in seat_data:
                continue
            mins = seat_data[seat_no]
            color = '#f4ad44' if mins <= window else '#3c4856'
            with col:
                st.markdown(f'''<div style="border-radius:10px;background:{color};color:white;padding:13px 3px;text-align:center;margin-bottom:6px"><b>{seat_no:02d}</b><div style="font-size:11px">{mins}분 후 예정</div></div>''', unsafe_allow_html=True)
    selected = st.selectbox('좌석별 종료 예정시간 조회', options=list(seat_data.keys()), format_func=lambda x:f'{x:02d}번 좌석')
    st.write(f'**{selected:02d}번 좌석:** {seat_data[selected]}분 뒤 예약 종료 예정 (가상 정보)')
    if st.button('관심 좌석 알림 설정 시연'):
        st.success('알림 설정 화면 시연 완료. 실제 푸시 알림은 연결되지 않음.')

with page3:
    st.subheader('외출 복귀 알림 시연')
    st.write('이용자가 외출 시작과 허용시간을 직접 입력하는 독립형 시연 기능임.')
    allowed = st.number_input('외출 허용시간 (분)', min_value=10, max_value=180, value=50, step=5)
    warn = st.number_input('복귀 알림을 받을 시점 (종료 몇 분 전)', min_value=1, max_value=30, value=10)
    if st.button('지금 외출 시작'):
        st.session_state['out_start'] = datetime.now()
    start_time = st.session_state.get('out_start')
    if start_time:
        end = start_time + timedelta(minutes=allowed)
        st.success(f'외출 시작: {start_time:%H:%M:%S} / 복귀 기한: {end:%H:%M:%S}')
        st.write(f'복귀 알림 예정: {(end - timedelta(minutes=warn)):%H:%M:%S}')
        st.caption('브라우저를 닫은 상태의 자동 알림은 지원하지 않는 시연용 기능임.')
    else:
        st.info('버튼을 누르면 외출 종료 및 복귀 알림 예정시간을 계산함.')

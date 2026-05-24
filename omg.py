import streamlit as st

st.set_page_config(
    page_title="HMinh Technology Solutions",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.8rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        border-top: 4px solid #0284c7;
        transition: 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    .metric-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0284c7;
        margin-bottom: 0.2rem;
    }
    .metric-label {
        font-size: 1rem;
        color: #475569;
        font-weight: 500;
    }
    .feature-card {
        background: white;
        padding: 1.8rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 4px solid #0f172a;
        height: 100%;
    }
    .feature-card h3 {
        margin-top: 0;
        font-size: 1.2rem;
        color: #0f172a;
    }
    .feature-card p {
        color: #566573;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .stApp {
        background-color: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📌 Hệ thống HMinh")
    st.markdown("Cổng thông tin & Điều hướng điện tử")
    
    page_options = ["Trang Chủ", "Phân Tích Dữ Liệu", "Cấu Hình Hệ Thống"]
    selected_page = st.selectbox("Lựa chọn phân hệ:", page_options, index=0)
    
    st.markdown("---")
    if st.button("Làm mới hệ thống", type="secondary", use_container_width=True):
        st.rerun()
        
    st.markdown("---")
    st.caption("Phiên bản Enterprise v1.0.0")
    st.info("Hệ thống được bảo mật và vận hành bởi HMinh Co., Ltd.")

if selected_page == "Trang Chủ":
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<h1 class="main-header">HMinh Technology Solutions</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Bứt phá giới hạn công nghệ - Nâng tầm giá trị doanh nghiệp</p>', unsafe_allow_html=True)

    banner_col1, banner_col2 = st.columns([3, 1])
    with banner_col1:
        st.success("💡 **Thông báo mới:** HMinh chính thức ra mắt giải pháp tối ưu hóa dữ liệu doanh nghiệp ứng dụng AI thế hệ mới.")
    with banner_col2:
        if st.button("Đăng ký tư vấn giải pháp", type="primary", use_container_width=True):
            st.toast("Cảm ơn bạn đã quan tâm. Hệ thống sẽ liên hệ lại trong vòng 24h làm việc!", icon="✅")

    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1e293b; font-size: 1.8rem; margin-bottom: 1.5rem;'>Chỉ Số Năng Lực Trọng Yếu</h2>", unsafe_allow_html=True)
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown('<div class="metric-card"><div class="metric-number">500+</div><div class="metric-label">Dự Án Triển Khai</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown('<div class="metric-card"><div class="metric-number">99.9%</div><div class="metric-label">Tỉ Lệ Uptime Hệ Thống</div></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown('<div class="metric-card"><div class="metric-number">98%</div><div class="metric-label">Khách Hàng Hài Lòng</div></div>', unsafe_allow_html=True)
    with m_col4:
        st.markdown('<div class="metric-card"><div class="metric-number">24/7</div><div class="metric-label">Hỗ Trợ Kỹ Thuật</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1e293b; font-size: 1.8rem; margin-bottom: 1.5rem;'>Dịch Vụ Cốt Lõi</h2>", unsafe_allow_html=True)
    
    features_data = [
        {"icon": "⚡", "title": "Phát Triển Phần Mềm", "desc": "Xây dựng các hệ thống quản trị, ứng dụng web và mobile với hiệu suất tối ưu và kiến trúc mở mở rộng tốt."},
        {"icon": "🛡️", "title": "Bảo Mật Hệ Thống", "desc": "Giải pháp an toàn thông tin toàn diện, mã hóa dữ liệu end-to-end theo tiêu chuẩn quốc tế nghiêm ngặt."},
        {"icon": "🌐", "title": "Điện Toán Đám Mây", "desc": "Tư vấn cấu trúc, chuyển dịch dữ liệu hạ tầng doanh nghiệp lên Cloud an toàn, linh hoạt và tiết kiệm chi phí."},
        {"icon": "🤖", "title": "Tích Hợp Trí Tuệ Nhân Tạo", "desc": "Ứng dụng các mô hình học máy (Machine Learning) và AI tiên tiến giúp tự động hóa quy trình vận hành."}
    ]

    f_cols = st.columns(4)
    for i, feature in enumerate(features_data):
        with f_cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{feature['icon']} {feature['title']}</h3>
                <p>{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    about_col1, about_col2 = st.columns([5, 3])
    with about_col1:
        st.markdown("### 🏢 Về chúng tôi")
        st.markdown("""
        **HMinh Technology Solutions** là đơn vị tiên phong trong lĩnh vực tư vấn chuyển đổi số và cung cấp các giải pháp công nghệ thông tin chuyên sâu cho doanh nghiệp. 
        
        Chúng tôi cam kết đồng hành cùng các đối tác để tối ưu hóa quy trình vận hành nội bộ, tăng cường bảo mật thông tin và bứt phá hiệu suất kinh doanh bằng những xu hướng công nghệ mới nhất. Với đội ngũ kỹ sư tâm huyết và giàu kinh nghiệm, HMinh tự tin giải quyết triệt để các bài toán kỹ thuật phức tạp của thời đại số.
        """)
    with about_col2:
        st.markdown("### 🏆 Thành Tựu Đạt Được")
        st.markdown("- **Top 10** Đơn vị cung cấp giải pháp chuyển đổi số tiêu biểu.")
        st.markdown("- Chứng nhận tiêu chuẩn bảo mật dữ liệu và an toàn thông tin.")
        st.markdown("- Đối tác chiến lược toàn cầu của các đơn vị hạ tầng Cloud lớn.")

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background-color: #f1f5f9; border-radius: 12px; border: 1px solid #e2e8f0;'>
        <h4 style='color: #0f172a; margin-bottom: 0.5rem;'>LIÊN HỆ VỚI CHÚNG TÔI</h4>
        <p style='color: #475569; margin-bottom: 0.2rem;'><strong>Văn phòng đại diện:</strong> Tòa nhà Công nghệ HMinh, Hà Nội, Việt Nam</p>
        <p style='color: #475569; margin-bottom: 0.5rem;'><strong>Email điều hành:</strong> contact@hminhtech.com | <strong>Hotline tổng đài:</strong> (+84) 24 8888 9999</p>
        <p style='font-size: 0.9rem; color: #64748b;'>Website chính thức: <a href="https://hminhtech.com" target="_blank" style="color: #0284c7; text-decoration: none;">https://hminhtech.com</a></p>
    </div>
    """, unsafe_allow_html=True)

elif selected_page == "Phân Tích Dữ Liệu":
    st.header("📊 Phân Hệ Phân Tích Dữ Liệu")
    st.write("Giao diện tổng hợp số liệu kỹ thuật đang được cấu hình...")
    st.info("Vui lòng quay lại sau khi hệ thống hoàn tất kết nối cơ sở dữ liệu.")

elif selected_page == "Cấu Hình Hệ Thống":
    st.header("⚙️ Cấu Hình Hệ Thống")
    st.write("Khu vực quản lý thiết lập dành cho quản trị viên hệ thống HMinh.")
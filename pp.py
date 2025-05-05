# app.py
import streamlit as st
from streamlit.components.v1 import html
import json
from pyvis.network import Network
from datetime import datetime

st.set_page_config(page_title="CSHeroes", layout="wide")

# Combined CSS styles with fixed selectors
st.markdown("""
<style>
:root {
    --primary-color: #ecf0f1;
    --accent-color: #a259ec;
    --secondary-color: #38b6ff;
    --timeline-width: 4px;
    --card-radius: 18px;
    --text-light: #bdc3c7;
    --bg-default: #232946;
    --bg-surface: #2d3250;
    --bg-card: #3b4a5a;
    --glass-bg: rgba(255,255,255,0.12);
    --glass-blur: 18px;
    --shadow-main: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    --shadow-card: 0 6px 24px 0 rgba(52, 152, 219, 0.13);
    --gradient-main: linear-gradient(135deg, #a259ec 0%, #38b6ff 100%);
    --gradient-card: linear-gradient(120deg, #f8fafc 0%, #e0e7ef 100%);
    --scrollbar-thumb: #a259ec;
    --scrollbar-track: #232946;
}

body, .stApp {
    background: var(--bg-default) !important;
    color: var(--primary-color) !important;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
    letter-spacing: 0.01em;
}

.st-emotion-cache-6qob1r {
    background: var(--bg-surface) !important;
    box-shadow: var(--shadow-main) !important;
    padding: 1.5rem 2.5rem !important;
    border-radius: var(--card-radius) !important;
    backdrop-filter: blur(var(--glass-blur)) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

.stButton > button {
    background: var(--gradient-main) !important;
    color: #fff !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 16px rgba(162,89,236,0.18) !important;
    font-weight: 600;
    font-size: 1.1rem;
    padding: 0.7rem 2rem;
    border: none !important;
    transition: all 0.18s cubic-bezier(.4,0,.2,1);
    outline: none !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #38b6ff 0%, #a259ec 100%) !important;
    transform: translateY(-2px) scale(1.07);
    box-shadow: 0 8px 24px rgba(56,182,255,0.18) !important;
}

.hero {
    text-align: center;
    background: var(--glass-bg);
    border: 1px solid rgba(255,255,255,0.13);
    padding: 8rem 2rem 7rem 2rem;
    border-radius: var(--card-radius);
    margin: 2.5rem 1.5rem 2rem 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-main);
    backdrop-filter: blur(var(--glass-blur));
    animation: float 6s ease-in-out infinite;
}
.hero::before {
    content: '';
    position: absolute;
    width: 420px;
    height: 420px;
    background: var(--accent-color);
    opacity: 0.10;
    border-radius: 50%;
    filter: blur(120px);
    top: -120px;
    left: -120px;
    z-index: 0;
}
.hero::after {
    content: '';
    position: absolute;
    width: 320px;
    height: 320px;
    background: var(--secondary-color);
    opacity: 0.10;
    border-radius: 50%;
    filter: blur(100px);
    bottom: -100px;
    right: -100px;
    z-index: 0;
}
.welcome-text {
    -webkit-text-fill-color: transparent;
    background: var(--gradient-main);
    font-size: 4.5rem !important;
    color: var(--primary-color);
    margin-bottom: 1.5rem;
    position: relative;
    -webkit-background-clip: text;
    background-clip: text;
    font-weight: 800;
    letter-spacing: -1.5px;
    z-index: 1;
    text-shadow: 0 2px 24px rgba(162,89,236,0.13);
}
.tagline {
    color: var(--text-light);
    font-size: 1.6rem;
    margin-bottom: 3rem;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.7;
    z-index: 1;
}

.badge {
    background: var(--gradient-main);
    color: #fff;
    padding: 0.5rem 1.2rem;
    border-radius: 22px;
    font-size: 1rem;
    width: fit-content;
    border: 1px solid rgba(52, 152, 219, 0.18);
    box-shadow: 0 2px 8px rgba(162,89,236,0.08);
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.2rem;
    transition: background 0.2s;
}
.badge::before {
    content: '★';
    font-size: 1.1em;
    color: #fffbe7;
    margin-right: 0.4em;
    opacity: 0.7;
}

.filter-section {
    padding: 2rem 1.5rem;
    background: var(--glass-bg);
    border-radius: var(--card-radius);
    margin: 1.2rem 0;
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(0,0,0,0.07);
    backdrop-filter: blur(var(--glass-blur));
    transition: box-shadow 0.2s;
}
.filter-section:hover {
    box-shadow: 0 8px 32px rgba(56,182,255,0.13);
}

.progress-container {
    background: var(--glass-bg);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 2.2rem 2rem;
    border-radius: var(--card-radius);
    margin: 2.5rem auto 2rem auto;
    max-width: 850px;
    box-shadow: var(--shadow-card);
    backdrop-filter: blur(var(--glass-blur));
}
.progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1.2rem;
    color: var(--primary-color);
    font-weight: 600;
    font-size: 1.2rem;
}
.progress-bar {
    background: #3b4a5a;
    height: 14px;
    border-radius: 7px;
    overflow: hidden;
    margin-bottom: 0.7rem;
}
.progress-fill {
    background: var(--gradient-main);
    height: 100%;
    width: 85%;
    border-radius: 7px;
    transition: width 0.5s cubic-bezier(.4,0,.2,1);
    box-shadow: 0 2px 8px rgba(162,89,236,0.13);
}
.milestones {
    display: flex;
    justify-content: space-between;
    margin-top: 1.1rem;
    color: var(--text-light);
    font-size: 1.05rem;
}

.timeline-container {
    background: var(--glass-bg);
    border: 1px solid rgba(255,255,255,0.10);
    position: relative;
    max-width: 1400px;
    margin: 4rem auto 2rem auto;
    padding: 2.5rem 2rem;
    border-radius: var(--card-radius);
    box-shadow: var(--shadow-card);
    backdrop-filter: blur(var(--glass-blur));
}
.timeline-line, .timeline-track {
    position: absolute;
    left: 50%;
    width: var(--timeline-width);
    background: var(--accent-color);
    top: 0;
    bottom: 0;
    transform: translateX(-50%);
    z-index: 0;
    border-radius: 2px;
    opacity: 0.18;
}
.node-grid, .era-group {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 2.7rem;
    position: relative;
    z-index: 1;
    padding: 2.2rem 0;
}
.node-card, .concept-column {
    background: var(--gradient-card);
    padding: 2.2rem 1.5rem 1.7rem 1.5rem;
    border-radius: var(--card-radius);
    box-shadow: 0 10px 32px rgba(56,182,255,0.10);
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    cursor: pointer;
    position: relative;
    border-left: 5px solid var(--accent-color);
    min-height: 210px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: var(--gradient-card);
    overflow: hidden;
    animation: float 7s ease-in-out infinite;
}
.node-card:hover, .concept-column:hover {
    transform: translateY(-12px) scale(1.03) rotate(-1deg);
    box-shadow: 0 18px 40px rgba(162,89,236,0.18);
    border-left: 5px solid var(--secondary-color);
}

.modal-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.7rem;
}

.sub-concept {
    padding: 0.9rem 1.3rem;
    margin: 0.6rem 0;
    background: #f8f9fa;
    border-radius: 10px;
    display: flex;
    align-items: center;
    transition: all 0.22s cubic-bezier(.4,0,.2,1);
    border: 1px solid rgba(0,0,0,0.06);
    font-weight: 500;
    font-size: 1.08rem;
    box-shadow: 0 2px 8px rgba(56,182,255,0.06);
}
.sub-concept:hover {
    transform: translateX(7px) scale(1.03);
    background: rgba(56,182,255,0.08);
    color: var(--accent-color);
}
.sub-concept::before {
    content: '•';
    color: var(--accent-color);
    margin-right: 0.9rem;
    font-weight: bold;
    font-size: 1.2rem;
}

.connector-line {
    position: absolute;
    height: 2px;
    background: var(--accent-color);
    width: 20%;
    opacity: 0.18;
}
.left-connector { right: 100%; }
.right-connector { left: 100%; }

.back-to-top {
    position: fixed;
    bottom: 2.2rem;
    right: 2.2rem;
    background: var(--gradient-main);
    color: white;
    padding: 1.1rem;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 6px 18px rgba(162,89,236,0.13);
    transition: all 0.3s cubic-bezier(.4,0,.2,1);
    z-index: 1000;
    font-size: 1.5rem;
    border: none;
    outline: none;
    display: flex;
    align-items: center;
    justify-content: center;
}
.back-to-top:hover {
    transform: translateY(-7px) scale(1.13) rotate(-8deg);
    background: linear-gradient(135deg, #38b6ff 0%, #a259ec 100%);
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 10px;
    background: var(--scrollbar-track);
    border-radius: 8px;
}
::-webkit-scrollbar-thumb {
    background: var(--scrollbar-thumb);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(162,89,236,0.13);
}
::-webkit-scrollbar-thumb:hover {
    background: #38b6ff;
}

/* Modal Styles */
.modal {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(35,41,70,0.65);
    display: flex; justify-content: center; align-items: center;
    z-index: 2000;
    animation: fadeIn 0.3s;
}
.modal-content {
    background: var(--glass-bg);
    border-radius: 22px;
    box-shadow: var(--shadow-main);
    padding: 2.5rem 2rem 2rem 2rem;
    max-width: 600px;
    width: 95vw;
    position: relative;
    border: 1.5px solid rgba(255,255,255,0.13);
    backdrop-filter: blur(var(--glass-blur));
    animation: popIn 0.4s cubic-bezier(.4,0,.2,1);
}
.modal-content h2 {
    color: var(--accent-color);
    font-weight: 800;
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
}
.modal-content button {
    background: none;
    border: none;
    font-size: 2rem;
    color: var(--secondary-color);
    cursor: pointer;
    transition: color 0.2s;
}
.modal-content button:hover {
    color: #a259ec;
}
.modal-content .badge {
    margin-bottom: 1.2rem;
    font-size: 1.1rem;
}
.modal-content h4 {
    color: var(--secondary-color);
    margin-top: 0.5rem;
    font-weight: 700;
}
.modal-content p {
    color: var(--text-light);
    font-size: 1.08rem;
}

@keyframes float { 
    0% { transform: translateY(0px); } 
    50% { transform: translateY(-10px); } 
    100% { transform: translateY(0px); } 
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
@keyframes popIn {
    0% { transform: scale(0.85); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

@media (max-width: 900px) {
    .hero { padding: 5rem 0.5rem; }
    .welcome-text { font-size: 2.5rem !important; }
    .node-grid, .era-group { grid-template-columns: 1fr; }
    .modal-content { width: 98vw; padding: 1.2rem; }
    .timeline-track { display: none; }
    .stButton > button { width: 100%; margin: 0.5rem 0; }
}
</style>
""",
            unsafe_allow_html=True)

# Timeline Data for CS Concepts
timeline_data = [
    {
        "year": "1960s",
        "concepts": {
            "Arrays & Hashing": ["Two Pointers", "Stack"],
            "Binary Search": ["Sibling Window", "Linked List"]
        }
    },
    {
        "year": "1970s",
        "concepts": {
            "Trees": [],
            "Tries": ["Backtracking"]
        }
    },
    {
        "year": "1980s",
        "concepts": {
            "Heap/Priority Queue": [],
            "Graphs": ["1-D DP"]
        }
    },
    {
        "year": "1990s",
        "concepts": {
            "Intervals": ["Greedy"],
            "Advanced Graphs": ["2-D DP", "Bit Manipulation"]
        }
    },
]

# Enhanced Data Structure for Heroes
HEROES = [
    {
        "year": 1936,
        "name": "Alan Turing",
        "title": "Turing Machine",
        "description":
        "Introduced the concept of a universal machine that laid the foundation for modern computers.",
        "connections": [1945],
        "tags": ["Theory", "Computation", "Mathematics"],
        "impact": "Fundamental theory for modern CS",
        "resources": ["The Annotated Turing", "Turing's Original Paper"]
    },
    {
        "year": 1945,
        "name": "John von Neumann",
        "title": "Von Neumann Architecture",
        "description":
        "Developed the stored-program architecture still used today.",
        "connections": [1958],
        "tags": ["Architecture", "Hardware", "Systems"],
        "impact": "Basis for modern computer design",
        "resources": ["First Draft Report on the EDVAC"]
    },
    {
        "year": 1958,
        "name": "Jack Kilby & Robert Noyce",
        "title": "Integrated Circuit",
        "description":
        "Revolutionized electronics by inventing the integrated circuit.",
        "connections": [1971],
        "tags": ["Electronics", "Hardware", "Innovation"],
        "impact": "Enabled miniaturization of devices",
        "resources": ["Patent US3138743", "The Chip by T.R. Reid"]
    },
]

# Calculate Computer Science Timeline
cs_start_year = 1936  # Turing Machine invention
current_year = datetime.now().year
years_since_start = current_year - cs_start_year

# Sidebar & Navigation
page = st.sidebar.radio("Navigation",
                        ["Home", "History", "CS Concepts", "Discoveries"],
                        label_visibility="collapsed")
st.sidebar.markdown("---")
# Remove search and filter UI

# --- HOME PAGE ---
if page == "Home":
    # Inject Vanta.js black hole background using components.html for reliability
    html("""
    <div id='home-vanta-bg' style='position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;'></div>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r121/three.min.js'></script>
    <script src='https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.fog.min.js'></script>
    <script>
    window.addEventListener('DOMContentLoaded', function() {
      if (window.VANTA && window.THREE) {
        VANTA.FOG({
          el: "#home-vanta-bg",
          mouseControls: true,
          touchControls: true,
          minHeight: 200.00,
          minWidth: 200.00,
          highlightColor: 0xa259ec,
          midtoneColor: 0x232946,
          lowlightColor: 0x000000,
          baseColor: 0x000000,
          blurFactor: 0.7,
          speed: 1.2,
          zoom: 1.1
        });
      } else {
        setTimeout(function() {
          if (window.VANTA && window.THREE) {
            VANTA.FOG({
              el: "#home-vanta-bg",
              mouseControls: true,
              touchControls: true,
              minHeight: 200.00,
              minWidth: 200.00,
              highlightColor: 0xa259ec,
              midtoneColor: 0x232946,
              lowlightColor: 0x000000,
              baseColor: 0x000000,
              blurFactor: 0.7,
              speed: 1.2,
              zoom: 1.1
            });
          }
        }, 1200);
      }
    });
    </script>
    """,
         height=0)

    # --- 4K Universe Video (YouTube embed, reliable) ---
    st.markdown("""
    <div style='display:flex;justify-content:center;margin:2.5rem 0;'>
      <iframe width="900" height="420" src="https://www.youtube.com/embed/ztVV54sPOns?autoplay=1&mute=1&loop=1&controls=0&playlist=ztVV54sPOns" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen style="border-radius:22px;box-shadow:0 8px 32px 0 rgba(31,38,135,0.17);object-fit:cover;width:90vw;max-width:900px;"></iframe>
    </div>
    """,
                unsafe_allow_html=True)

    st.markdown("""
    <div class="home-content">
    """,
                unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <h1 class="welcome-text">CSHeroes</h1>
        <p class="tagline">Discover the Pioneers and Fundamental Concepts that Shaped Modern Computing</p>
        <div class="badge" style="margin: 0 auto;">Exploring {years} Years of Innovation</div>
    </div>
    """.format(years=years_since_start),
                unsafe_allow_html=True)

    # Digital timer since 1936
    html("""
    <div style='display:flex;justify-content:center;margin:2.5rem 0;'>
        <div id="cs-digital-timer" style="background:rgba(44,62,80,0.85);border-radius:18px;padding:2rem 3rem;box-shadow:0 4px 24px rgba(56,182,255,0.10);font-size:2.1rem;font-family:'Consolas','Menlo','monospace';color:#38b6ff;font-weight:900;letter-spacing:2px;text-align:center;">
            <span>⏳</span> <span id="cs-timer-value">Loading...</span><br>
            <span style='font-size:1.1rem;color:#a259ec;font-weight:600;'>Time since the birth of Computer Science (1936)</span>
        </div>
        </div>
    <script>
    function updateCSTimer() {
        const start = new Date(Date.UTC(1936, 0, 1, 0, 0, 0));
        const now = new Date();
        let diff = now - start;
        const years = now.getUTCFullYear() - 1936;
        const startOfThisYear = new Date(Date.UTC(now.getUTCFullYear(), 0, 1, 0, 0, 0));
        let days = Math.floor((now - startOfThisYear) / (1000*60*60*24));
        let hours = now.getUTCHours();
        let minutes = now.getUTCMinutes();
        let seconds = now.getUTCSeconds();
        document.getElementById('cs-timer-value').innerHTML = `${years} years, ${days} days, ${hours.toString().padStart(2,'0')}:${minutes.toString().padStart(2,'0')}:${seconds.toString().padStart(2,'0')}`;
    }
    setInterval(updateCSTimer, 1000);
    setTimeout(updateCSTimer, 100);
    </script>
    """,
         height=180)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="filter-section">
            <h3>📚 Core Concepts</h3>
            <p>Explore fundamental CS concepts through interactive timelines and visualizations</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="filter-section">
            <h3>👨💻 Pioneers</h3>
            <p>Discover the innovators who shaped modern computing</p>
        </div>
        """,
                    unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="filter-section">
            <h3>🚀 Innovations</h3>
            <p>Explore breakthrough technologies and their impacts</p>
        </div>
        """,
                    unsafe_allow_html=True)

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# --- HISTORY PAGE ---
elif page == "History":
    # 50+ discoveries/milestones
    HISTORY_DISCOVERIES = [
        {
            "year":
            1837,
            "name":
            "Analytical Engine",
            "desc":
            "Charles Babbage designs the first mechanical general-purpose computer."
        },
        {
            "year":
            1842,
            "name":
            "First Algorithm",
            "desc":
            "Ada Lovelace writes the first algorithm intended for a machine."
        },
        {
            "year": 1854,
            "name": "Boolean Algebra",
            "desc": "George Boole formalizes algebraic logic."
        },
        {
            "year": 1936,
            "name": "Turing Machine",
            "desc":
            "Alan Turing introduces the concept of a universal machine."
        },
        {
            "year": 1937,
            "name": "Digital Circuit Design",
            "desc": "Claude Shannon applies Boolean algebra to circuit design."
        },
        {
            "year": 1941,
            "name": "Z3 Computer",
            "desc":
            "Konrad Zuse builds the first programmable digital computer."
        },
        {
            "year": 1943,
            "name": "Colossus",
            "desc": "First programmable electronic digital computer (UK)."
        },
        {
            "year": 1945,
            "name": "Von Neumann Architecture",
            "desc": "John von Neumann describes the stored-program computer."
        },
        {
            "year": 1946,
            "name": "ENIAC",
            "desc": "First general-purpose electronic computer."
        },
        {
            "year": 1947,
            "name": "Transistor",
            "desc": "Bardeen, Brattain, and Shockley invent the transistor."
        },
        {
            "year": 1950,
            "name": "Turing Test",
            "desc": "Alan Turing proposes a test for machine intelligence."
        },
        {
            "year": 1951,
            "name": "UNIVAC I",
            "desc": "First commercially produced computer in the US."
        },
        {
            "year": 1952,
            "name": "Compiler",
            "desc": "Grace Hopper develops the first compiler (A-0)."
        },
        {
            "year": 1953,
            "name": "IBM 701",
            "desc": "IBM's first commercial scientific computer."
        },
        {
            "year": 1956,
            "name": "AI Term Coined",
            "desc": "John McCarthy coins the term 'Artificial Intelligence'."
        },
        {
            "year": 1956,
            "name": "Hard Disk",
            "desc": "IBM invents the first hard disk drive."
        },
        {
            "year": 1957,
            "name": "FORTRAN",
            "desc": "First high-level programming language."
        },
        {
            "year": 1958,
            "name": "Integrated Circuit",
            "desc": "Kilby & Noyce invent the integrated circuit."
        },
        {
            "year": 1959,
            "name": "COBOL",
            "desc": "Grace Hopper helps develop COBOL language."
        },
        {
            "year": 1960,
            "name": "ALGOL",
            "desc": "ALGOL language influences many modern languages."
        },
        {
            "year": 1962,
            "name": "Spacewar!",
            "desc": "First computer video game."
        },
        {
            "year": 1964,
            "name": "BASIC",
            "desc": "Beginner's All-purpose Symbolic Instruction Code."
        },
        {
            "year": 1965,
            "name": "Moore's Law",
            "desc": "Gordon Moore predicts exponential growth of transistors."
        },
        {
            "year": 1969,
            "name": "ARPANET",
            "desc":
            "First message sent over the ARPANET (precursor to Internet)."
        },
        {
            "year": 1970,
            "name": "UNIX",
            "desc": "Ken Thompson and Dennis Ritchie create UNIX OS."
        },
        {
            "year": 1971,
            "name": "Email",
            "desc": "Ray Tomlinson sends the first email."
        },
        {
            "year": 1972,
            "name": "C Language",
            "desc": "Dennis Ritchie develops C programming language."
        },
        {
            "year": 1973,
            "name": "Ethernet",
            "desc": "Robert Metcalfe invents Ethernet networking."
        },
        {
            "year": 1976,
            "name": "Apple I",
            "desc": "Steve Wozniak and Steve Jobs build the Apple I."
        },
        {
            "year": 1977,
            "name": "Personal Computer",
            "desc": "Apple II and Commodore PET popularize PCs."
        },
        {
            "year": 1978,
            "name": "RSA Encryption",
            "desc": "Rivest, Shamir, Adleman invent public-key cryptography."
        },
        {
            "year": 1981,
            "name": "IBM PC",
            "desc": "IBM launches its first personal computer."
        },
        {
            "year": 1983,
            "name": "DNS",
            "desc": "Domain Name System is introduced."
        },
        {
            "year": 1984,
            "name": "Macintosh",
            "desc": "Apple launches the Macintosh with GUI."
        },
        {
            "year": 1985,
            "name": "Windows 1.0",
            "desc": "Microsoft releases Windows 1.0."
        },
        {
            "year": 1989,
            "name": "World Wide Web",
            "desc": "Tim Berners-Lee invents the Web."
        },
        {
            "year": 1991,
            "name": "Linux",
            "desc": "Linus Torvalds releases Linux kernel."
        },
        {
            "year": 1993,
            "name": "Mosaic Browser",
            "desc": "First popular web browser."
        },
        {
            "year": 1995,
            "name": "Java",
            "desc": "Sun Microsystems releases Java."
        },
        {
            "year": 1995,
            "name": "JavaScript",
            "desc": "Brendan Eich creates JavaScript."
        },
        {
            "year": 1997,
            "name": "Deep Blue",
            "desc": "IBM's Deep Blue defeats chess champion Garry Kasparov."
        },
        {
            "year": 1998,
            "name": "Google Founded",
            "desc": "Larry Page and Sergey Brin found Google."
        },
        {
            "year": 2001,
            "name": "Wikipedia",
            "desc": "Wikipedia launches as a free online encyclopedia."
        },
        {
            "year": 2004,
            "name": "Facebook",
            "desc": "Mark Zuckerberg launches Facebook."
        },
        {
            "year": 2005,
            "name": "YouTube",
            "desc": "YouTube video sharing platform launches."
        },
        {
            "year": 2006,
            "name": "Cloud Computing",
            "desc": "Amazon launches AWS, popularizing cloud computing."
        },
        {
            "year": 2007,
            "name": "iPhone",
            "desc": "Apple releases the first iPhone."
        },
        {
            "year": 2008,
            "name": "Blockchain",
            "desc": "Bitcoin and blockchain technology introduced."
        },
        {
            "year": 2012,
            "name": "Deep Learning",
            "desc": "Breakthroughs in neural networks and AI."
        },
        {
            "year": 2016,
            "name": "AlphaGo",
            "desc": "Google DeepMind's AlphaGo defeats Go champion."
        },
        {
            "year": 2019,
            "name": "Quantum Supremacy",
            "desc": "Google claims quantum supremacy."
        },
        {
            "year": 2022,
            "name": "ChatGPT",
            "desc": "OpenAI releases ChatGPT, a powerful conversational AI."
        },
        # Add more to reach 50+
        {
            "year": 1950,
            "name": "First Computer Bug",
            "desc": "Grace Hopper finds a moth in a computer relay."
        },
        {
            "year":
            1968,
            "name":
            "Mother of All Demos",
            "desc":
            "Douglas Engelbart demonstrates the mouse, hypertext, and more."
        },
        {
            "year": 1970,
            "name": "Relational Databases",
            "desc": "Edgar F. Codd proposes the relational database model."
        },
        {
            "year": 1979,
            "name": "VisiCalc",
            "desc": "First spreadsheet program for personal computers."
        },
        {
            "year": 1982,
            "name": "CD-ROM",
            "desc": "Sony and Philips introduce the CD-ROM."
        },
        {
            "year": 1988,
            "name": "Morris Worm",
            "desc": "First major computer worm spreads on the Internet."
        },
        {
            "year": 1990,
            "name": "Photoshop",
            "desc": "Adobe releases Photoshop 1.0."
        },
        {
            "year": 1994,
            "name": "Amazon Founded",
            "desc": "Jeff Bezos founds Amazon.com."
        },
        {
            "year": 1999,
            "name": "Wi-Fi",
            "desc": "Wi-Fi Alliance forms, popularizing wireless networking."
        },
        {
            "year": 2000,
            "name": "USB Flash Drive",
            "desc": "First USB flash drives become available."
        },
        {
            "year": 2003,
            "name": "MySpace",
            "desc": "MySpace social network launches."
        },
        {
            "year": 2010,
            "name": "Instagram",
            "desc": "Instagram photo sharing app launches."
        },
        {
            "year": 2014,
            "name": "Apple Pay",
            "desc": "Apple introduces mobile payment system."
        },
        {
            "year": 2018,
            "name": "GDPR",
            "desc": "General Data Protection Regulation takes effect in EU."
        },
        {
            "year":
            2020,
            "name":
            "Remote Work Boom",
            "desc":
            "COVID-19 pandemic accelerates remote work and digital transformation."
        },
    ]

    # Sort by year
    HISTORY_DISCOVERIES.sort(key=lambda x: x['year'])

    # Minimalist timeline CSS
    st.markdown('''
    <style>
    .timeline-min {
        max-width: 700px;
        margin: 2.5rem auto 2rem auto;
        padding: 0 1.2rem;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .timeline-event {
        display: flex;
        align-items: flex-start;
        gap: 1.5rem;
        padding: 1.2rem 0;
        border-bottom: 1px solid #e0e7ef33;
        transition: background 0.15s;
    }
    .timeline-event:last-child {
        border-bottom: none;
    }
    .timeline-year {
        min-width: 70px;
        font-size: 1.25rem;
        font-weight: 700;
        color: #a259ec;
        opacity: 0.95;
        letter-spacing: 0.5px;
        text-align: right;
        flex-shrink: 0;
    }
    .timeline-content {
        flex: 1;
    }
    .timeline-title {
        font-size: 1.13rem;
        font-weight: 700;
        color: #232946;
        margin-bottom: 0.18rem;
    }
    .timeline-desc {
        color: #5c6273;
        font-size: 1.01rem;
        line-height: 1.6;
        margin-bottom: 0;
    }
    @media (max-width: 700px) {
        .timeline-min { padding: 0 0.2rem; }
        .timeline-year { min-width: 54px; font-size: 1.05rem; }
        .timeline-title { font-size: 1.01rem; }
    }
    </style>
    ''',
                unsafe_allow_html=True)

    st.markdown("""
    <div class='timeline-min'>
        <h1 style='text-align:center;font-size:2.1rem;font-weight:900;color:#a259ec;margin-bottom:2.2rem;'>Minimalist History of Computer Science</h1>
    """,
                unsafe_allow_html=True)
    for d in HISTORY_DISCOVERIES:
        st.markdown(f"""
        <div class='timeline-event'>
            <div class='timeline-year'>{d['year']}</div>
            <div class='timeline-content'>
                <div class='timeline-title'>{d['name']}</div>
                <div class='timeline-desc'>{d['desc']}</div>
            </div>
        </div>
        """,
                    unsafe_allow_html=True)
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# --- CS CONCEPTS PAGE ---
elif page == "CS Concepts":
    # Data structure info with theory, history, and images
    DATA_STRUCTURES = [
        {
            "name": "Array",
            "theory":
            "An array is a collection of items stored at contiguous memory locations. It allows fast access by index and is the simplest and most fundamental data structure in computer science. Arrays are used to implement other data structures and are the backbone of memory management in programming.",
            "history":
            "The concept of the array dates back to the earliest days of computer science. Arrays were formalized as a data structure in the 1940s, with John von Neumann's work on the EDVAC and the stored-program computer. Arrays became a core part of programming languages like FORTRAN (1957), which used them for scientific computing. Their simplicity and efficiency have made them a staple in nearly every programming language since.",
            "image":
            "https://usemynotes.com/wp-content/uploads/2021/02/what-are-arrays-in-java.jpg",
            "image_caption":
            "A simple array structure. Source: Wikimedia Commons"
        },
        {
            "name": "Linked List",
            "theory":
            "A linked list is a linear collection of data elements, called nodes, where each node points to the next. Unlike arrays, linked lists do not require contiguous memory and allow efficient insertions and deletions. There are several types: singly, doubly, and circular linked lists.",
            "history":
            "The linked list was first described by Allen Newell, Cliff Shaw, and Herbert Simon in 1955 as part of their work on the Logic Theory Machine and the Information Processing Language (IPL). Linked lists were revolutionary because they allowed dynamic memory allocation and flexible data management, influencing the design of LISP (1958), one of the earliest programming languages.",
            "image":
            "https://upload.wikimedia.org/wikipedia/commons/6/6d/Singly-linked-list.svg",
            "image_caption": "A singly linked list. Source: Wikimedia Commons"
        },
        {
            "name": "Stack",
            "theory":
            "A stack is a linear data structure that follows the Last In, First Out (LIFO) principle. Elements are added and removed from the top. Stacks are used for function calls, expression evaluation, undo operations, and more.",
            "history":
            "The stack was introduced by Friedrich L. Bauer in 1955. It became fundamental in the design of programming languages and computer architectures, especially for managing function calls and recursion. The concept of the call stack is central to modern computing, enabling structured programming and efficient memory use.",
            "image":
            "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lifo_stack.png",
            "image_caption":
            "Stack (LIFO) structure. Source: Wikimedia Commons"
        },
        {
            "name": "Queue",
            "theory":
            "A queue is a linear data structure that follows the First In, First Out (FIFO) principle. Elements are added at the rear and removed from the front. Queues are used in scheduling, buffering, and breadth-first search algorithms.",
            "history":
            "The queue concept was formalized by Alan Turing in 1936 in his work on the Turing Machine, which used an infinite tape as a queue. Queues became essential in operating systems for process scheduling and in networking for managing data packets. Their simplicity and efficiency make them a core part of computer science.",
            "image":
            "https://upload.wikimedia.org/wikipedia/commons/5/52/Data_Queue.svg",
            "image_caption":
            "Queue (FIFO) structure. Source: Wikimedia Commons"
        },
        {
            "name":
            "Hash Table",
            "theory":
            "A hash table is a data structure that maps keys to values for highly efficient lookup. It uses a hash function to compute an index into an array of buckets, from which the desired value can be found.",
            "history":
            "The hash table was invented by Hans Peter Luhn at IBM in 1953. Hashing revolutionized data retrieval, enabling constant-time average-case access. Hash tables are now used in databases, caches, and language runtimes, and are the basis for objects and dictionaries in many programming languages.",
            "image":
            "https://cdn.testbook.com/images/seo/hash-function-in-data-structure.png",
            "image_caption":
            "Hash table with linked list collision resolution. Source: Wikimedia Commons"
        },
        {
            "name": "Tree",
            "theory":
            "A tree is a hierarchical data structure consisting of nodes, with a single root and potentially many levels of additional nodes. Trees are used for searching, sorting, representing hierarchies, and more. Common types include binary trees, AVL trees, and B-trees.",
            "history":
            "The mathematical concept of trees was introduced by Arthur Cayley in 1857, but their use in computer science began in the 1950s with the development of file systems and databases. Trees became essential for organizing data efficiently, enabling fast search and retrieval, and are the foundation of many algorithms and data structures today.",
            "image":
            "https://upload.wikimedia.org/wikipedia/commons/f/f7/Binary_tree.svg",
            "image_caption": "A binary tree. Source: Wikimedia Commons"
        },
    ]

    st.markdown("""
    <style>
    .ds-card {
        background: linear-gradient(120deg, #f8fafc 0%, #e0e7ef 100%);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(56,182,255,0.13);
        padding: 2.5rem 2rem 2rem 2rem;
        margin-bottom: 2.5rem;
        margin-top: 1.5rem;
        position: relative;
        transition: box-shadow 0.25s, transform 0.25s;
        border-left: 6px solid #a259ec;
        overflow: hidden;
    }
    .ds-card:hover {
        box-shadow: 0 18px 48px rgba(162,89,236,0.18);
        transform: translateY(-8px) scale(1.02);
        border-left: 6px solid #38b6ff;
    }
    .ds-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #232946;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .ds-intro {
        color: #34495e;
        font-size: 1.15rem;
        margin-bottom: 1.5rem;
        line-height: 1.7;
    }
    .ds-history {
        color: #5c6273;
        font-size: 1.08rem;
        margin-bottom: 1.2rem;
        line-height: 1.6;
    }
    .ds-img {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0 0.5rem 0;
    }
    .ds-img img {
        max-width: 340px;
        width: 100%;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(56,182,255,0.08);
        background: #fff;
        padding: 0.5rem;
    }
    .ds-img-caption {
        text-align: center;
        color: #a259ec;
        font-size: 0.98rem;
        margin-bottom: 1.2rem;
    }
    </style>
    """,
                unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-top:2rem; margin-bottom:2rem;'>
        <h1 style='font-size:2.8rem; font-weight:900; color:#a259ec; letter-spacing:-2px;'>Data Structures: Theory & History</h1>
        <p style='color:#34495e; font-size:1.3rem; max-width:700px; margin:0 auto;'>
            Discover the most fundamental data structures in computer science. Read their theory, explore their rich history, and see how they are visualized!
        </p>
    </div>
    """,
                unsafe_allow_html=True)

    for ds in DATA_STRUCTURES:
        st.markdown(f"""
        <div class='ds-card'>
            <div class='ds-title'>{ds['name']}</div>
            <div class='ds-intro'>{ds['theory']}</div>
            <div class='ds-history'><b>History:</b> {ds['history']}</div>
            <div class='ds-img'>
                <img src='{ds['image']}' alt='{ds['name']} diagram'>
            </div>
            <div class='ds-img-caption'>{ds['image_caption']}</div>
        </div>
        """,
                    unsafe_allow_html=True)

# --- DISCOVERIES PAGE ---
elif page == "Discoveries":
    st.markdown("## 📜 Computer Science Discoveries Timeline")

    # Expanded and enhanced discoveries
    DISCOVERIES = [
        {
            "id": "Boolean Algebra",
            "year": 1854,
            "desc": "George Boole's algebraic logic"
        },
        {
            "id": "Analytical Engine",
            "year": 1837,
            "desc": "Charles Babbage's mechanical general-purpose computer"
        },
        {
            "id": "Turing Machine",
            "year": 1936,
            "desc": "Alan Turing's universal machine"
        },
        {
            "id": "ENIAC",
            "year": 1945,
            "desc": "First general-purpose electronic computer"
        },
        {
            "id": "Von Neumann Arch.",
            "year": 1945,
            "desc": "Stored-program computer"
        },
        {
            "id": "Transistor",
            "year": 1947,
            "desc": "Invention of the transistor (Bardeen, Brattain, Shockley)"
        },
        {
            "id": "Integrated Circuit",
            "year": 1958,
            "desc": "Kilby & Noyce's integrated circuit"
        },
        {
            "id": "UNIX",
            "year": 1970,
            "desc": "Birth of UNIX operating system"
        },
        {
            "id": "Internet",
            "year": 1969,
            "desc": "ARPANET, the precursor to the Internet"
        },
        {
            "id": "C Language",
            "year": 1972,
            "desc": "Dennis Ritchie's C programming language"
        },
        {
            "id": "Personal Computer",
            "year": 1977,
            "desc": "Apple II and the PC revolution"
        },
        {
            "id": "World Wide Web",
            "year": 1989,
            "desc": "Tim Berners-Lee invents the Web"
        },
        {
            "id": "Linux",
            "year": 1991,
            "desc": "Linus Torvalds releases Linux kernel"
        },
        {
            "id": "Deep Learning",
            "year": 2012,
            "desc": "Breakthroughs in neural networks and AI"
        },
        {
            "id": "Quantum Computing",
            "year": 2019,
            "desc": "Google claims quantum supremacy"
        },
        {
            "id": "Blockchain",
            "year": 2008,
            "desc": "Bitcoin and the rise of blockchain technology"
        },
        {
            "id": "Cloud Computing",
            "year": 2006,
            "desc": "Amazon AWS launches, popularizing cloud computing"
        },
        {
            "id": "Mobile Revolution",
            "year": 2007,
            "desc": "Apple iPhone and the mobile era"
        },
        {
            "id": "AI Ethics",
            "year": 2016,
            "desc": "Growing focus on ethics in AI and technology"
        },
    ]
    EDGES = [
        ("Analytical Engine", "Boolean Algebra"),
        ("Boolean Algebra", "Turing Machine"),
        ("Turing Machine", "ENIAC"),
        ("ENIAC", "Von Neumann Arch."),
        ("Von Neumann Arch.", "Transistor"),
        ("Transistor", "Integrated Circuit"),
        ("Integrated Circuit", "Personal Computer"),
        ("Personal Computer", "UNIX"),
        ("UNIX", "C Language"),
        ("UNIX", "Linux"),
        ("UNIX", "Internet"),
        ("Internet", "World Wide Web"),
        ("World Wide Web", "Deep Learning"),
        ("Deep Learning", "Quantum Computing"),
        ("Linux", "Deep Learning"),
        ("Personal Computer", "World Wide Web"),
        ("Integrated Circuit", "Internet"),
        ("World Wide Web", "Cloud Computing"),
        ("Cloud Computing", "AI Ethics"),
        ("Blockchain", "AI Ethics"),
        ("Mobile Revolution", "Cloud Computing"),
        ("Cloud Computing", "Deep Learning"),
        ("Blockchain", "Cloud Computing"),
    ]

    net = Network(height="750px",
                  width="100%",
                  directed=True,
                  bgcolor="#00000000",
                  font_color="#ecf0f1")
    net.toggle_physics(True)
    net.barnes_hut(gravity=-25000,
                   central_gravity=0.3,
                   spring_length=180,
                   spring_strength=0.03,
                   damping=0.85)

    for d in DISCOVERIES:
        net.add_node(
            d["id"],
            label=f"{d['id']}\n({d['year']})",
            title=d["desc"],
            shape="box",
            color={
                "background":
                "#38b6ff" if d["year"] > 2000 else
                ("#a259ec" if d["year"] > 1980 else
                 ("#f7b731" if d["year"] > 1940 else "#ffb347")),
                "border":
                "#fff",
                "highlight": {
                    "background": "#a259ec",
                    "border": "#fff"
                },
            },
            borderWidth=3,
            shadow=True,
            font={
                "size": 22,
                "face": "Segoe UI",
                "color": "#232946"
            },
        )

    for src, dst in EDGES:
        net.add_edge(
            src,
            dst,
            color="#a259ec",
            width=3,
            arrowStrikethrough=False,
            smooth={"type": "cubicBezier"},
        )

    net.set_options("""
    {
      "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "color": {
          "border": "#fff",
          "highlight": {
            "border": "#38b6ff",
            "background": "#a259ec"
          }
        },
        "font": {
          "color": "#232946",
          "size": 22,
          "face": "Segoe UI",
          "strokeWidth": 0
        },
        "shadow": true,
        "shape": "box",
        "margin": 12
      },
      "edges": {
        "color": "#a259ec",
        "width": 3,
        "smooth": {
          "type": "cubicBezier",
          "roundness": 0.5
        },
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 1.2
          }
        },
        "shadow": true
      },
      "layout": {
        "improvedLayout": true,
        "hierarchical": false
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -25000,
          "centralGravity": 0.3,
          "springLength": 180,
          "springConstant": 0.03,
          "damping": 0.85,
          "avoidOverlap": 1
        },
        "stabilization": {
          "enabled": true,
          "iterations": 200,
          "updateInterval": 25
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 120,
        "navigationButtons": true,
        "keyboard": true,
        "multiselect": true,
        "dragNodes": true,
        "dragView": true,
        "zoomView": true
      },
      "manipulation": {
        "enabled": false
      }
    }
    """)

    net.save_graph("discoveries.html")
    # 4K static backgrounds for topics (replace with your own URLs if desired)
    topic_backgrounds = {
        "Quantum Computing":
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80",
        "Deep Learning":
        "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80",
        "Blockchain":
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1500&q=80",
        "Cloud Computing":
        "https://images.unsplash.com/photo-1465101178521-c1a9136a3b99?auto=format&fit=crop&w=1500&q=80",
        "World Wide Web":
        "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80"
        # Add more as needed
    }

    with open("discoveries.html", 'r', encoding='utf-8') as f:
        html_code = f.read()

    inject = f'''
    <style>
    body, html, #universe-bg {{ height: 100% !important; width: 100% !important; margin: 0; padding: 0; overflow: hidden; }}
    #universe-bg {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; }}
    #static-bg {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; opacity: 0; transition: opacity 0.7s; background-size: cover; background-position: center; pointer-events: none; }}
    #mynetwork {{ position: relative; z-index: 2; }}
    </style>
    <div id="universe-bg"></div>
    <div id="static-bg"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r121/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"></script>
    <script>
    let vantaEffect = null;
    function startVanta() {{
      if (vantaEffect) vantaEffect.destroy();
      vantaEffect = VANTA.NET({{
        el: "#universe-bg",
        mouseControls: true,
        touchControls: true,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0xa259ec,
        backgroundColor: 0x232946,
        points: 14.0,
        maxDistance: 22.0,
        spacing: 18.0
      }});
    }}
    startVanta();
    // Listen for node clicks
    setTimeout(function() {{
      var network = window.network || window.visNetwork;
      if (!network && window['mynetwork']) network = window['mynetwork'];
      if (!network) return;
      network.on('click', function(params) {{
        if (params.nodes && params.nodes.length > 0) {{
          var nodeId = params.nodes[0];
          var topicImages = {json.dumps(topic_backgrounds)};
          if (topicImages[nodeId]) {{
            document.getElementById('static-bg').style.backgroundImage = 'url(' + topicImages[nodeId] + ')';
            document.getElementById('static-bg').style.opacity = 1;
            if (vantaEffect) vantaEffect.pause();
            setTimeout(function() {{
              document.getElementById('static-bg').style.opacity = 0;
              if (vantaEffect) vantaEffect.resume && vantaEffect.resume();
            }}, 10000);
          }}
        }}
      }});
    }}, 1200);
    </script>
    '''

    if '</body>' in html_code:
        html_code = html_code.replace('</body>', inject + '</body>')
    else:
        html_code += inject

    st.components.v1.html(html_code, height=800)

# --- MODAL JAVASCRIPT ---
modal_js = f"""
<script>
const HEROES = {json.dumps(HEROES)};

function showAdvancedModal(name) {{
    const hero = HEROES.find(h => h.name === name);
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;">
                <h2 style="margin:0;">${{hero.name}}</h2>
                <button onclick="this.parentElement.parentElement.parentElement.remove()" 
                    title="Close">×</button>
            </div>
            <div class="badge" style="margin-bottom:1rem;">${{hero.title}}</div>
            <p style="color:var(--text-light); line-height:1.6;">${{hero.description}}</p>
            <div style="margin:2rem 0;">
                <h4>🔗 Historical Connections</h4>
                <div style="display:flex; gap:0.5rem; margin-top:1rem;">
                    ${{hero.connections.map(c => `<div class='badge'>${{c}}</div>`).join('')}}
                </div>
            </div>
            <div style="background:rgba(56,182,255,0.08); padding:1.5rem; border-radius:12px; box-shadow:0 2px 8px rgba(56,182,255,0.08);">
                <h4 style="margin-top:0;">✨ Impact on Computing</h4>
                <p style="margin-bottom:0;">${{hero.impact}}</p>
            </div>
            <div style="margin-top:2rem;">
                <h4>📚 Resources</h4>
                <ul style="padding-left:1.2rem; color:var(--secondary-color);">
                    ${{hero.resources.map(r => `<li style='margin-bottom:0.3rem;'>${{r}}</li>`).join('')}}
                </ul>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}}
// Close modal when clicking outside
setTimeout(() => {{
document.addEventListener('click', function(event) {{
    if(event.target.className === 'modal') {{
        event.target.remove();
    }}
}});
}}, 100);
</script>
"""

html(modal_js)

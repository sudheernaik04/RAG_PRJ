def get_styles() -> str:
    return """
    <style>
        .main {
            background: #f5f7fb;
        }
        .stApp {
            background: linear-gradient(180deg, #f7f9fd 0%, #eef5ff 100%);
            color: #1f2937;
        }
        .card {
            background: white;
            padding: 1rem 1.2rem;
            border-radius: 14px;
            border: 1px solid #dfe7f3;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.8rem;
        }
        .status-ok {
            background: #eafaf1;
            color: #0f7a43;
        }
        .status-warn {
            background: #fff3d6;
            color: #8a5b00;
        }
        .status-bad {
            background: #ffe7e7;
            color: #a92b2b;
        }
        .small-caption {
            color: #53657d;
            font-size: 0.82rem;
        }
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }
    </style>
    """

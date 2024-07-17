def trimStr(s):
    """Trims given str down to alphanumeric characters"""
    trimmed=""
    for st in s:
        if st.isalnum() or st==" ":
            trimmed+=st.lower()
    return trimmed

def parsePrice(p):
    """Parses str p, which is formatted as $(price)/n, into a float"""
    price=float(p[2:-1])
    return price



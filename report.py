"""
report.py
Generates an HTML report showing the current status of the library:
all books, stock levels, and currently issued books.
This is what ties in the HTML skill alongside Python and SQL.
"""

from datetime import datetime
import database


def generate_html_report(filename="library_report.html"):
    books = database.get_all_books()
    issued = database.get_currently_issued_books()
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Library Status Report</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f7f7f7; color: #222; }}
    h1 {{ color: #2c3e50; }}
    h2 {{ color: #34495e; margin-top: 40px; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    th, td {{ padding: 10px 14px; border: 1px solid #ddd; text-align: left; }}
    th {{ background: #2c3e50; color: #fff; }}
    tr:nth-child(even) {{ background: #f2f2f2; }}
    .low-stock {{ color: #c0392b; font-weight: bold; }}
    .timestamp {{ color: #777; font-size: 0.9em; }}
</style>
</head>
<body>
    <h1>📚 Library Status Report</h1>
    <p class="timestamp">Generated on: {generated_on}</p>

    <h2>All Books ({len(books)} titles)</h2>
    <table>
        <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Genre</th>
            <th>Total Copies</th>
            <th>Available Copies</th>
        </tr>
"""

    for book in books:
        low_stock_class = ' class="low-stock"' if book["available_copies"] == 0 else ""
        html += f"""        <tr>
            <td>{book['title']}</td>
            <td>{book['author']}</td>
            <td>{book['genre'] or '-'}</td>
            <td>{book['total_copies']}</td>
            <td{low_stock_class}>{book['available_copies']}</td>
        </tr>
"""

    html += f"""    </table>

    <h2>Currently Issued Books ({len(issued)})</h2>
    <table>
        <tr>
            <th>Book Title</th>
            <th>Issued To</th>
            <th>Issue Date</th>
        </tr>
"""

    if issued:
        for row in issued:
            html += f"""        <tr>
            <td>{row['title']}</td>
            <td>{row['member_name']}</td>
            <td>{row['issue_date']}</td>
        </tr>
"""
    else:
        html += '        <tr><td colspan="3">No books currently issued.</td></tr>\n'

    html += """    </table>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    return filename

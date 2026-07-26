import sqlite3
from typing import Optional, Tuple, List, Dict
from app.config import settings


class BookService:
    """
    Data Access Service querying stored book records.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.DATABASE_PATH

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_books(
        self,
        page: int = 1,
        limit: int = 20,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[int] = None,
        sort_by: Optional[str] = None,
    ) -> Tuple[int, List[Dict]]:
        conn = self._get_connection()
        cursor = conn.cursor()

        where_clauses = []
        params = []

        if min_price is not None:
            where_clauses.append("price >= ?")
            params.append(min_price)
        if max_price is not None:
            where_clauses.append("price <= ?")
            params.append(max_price)
        if min_rating is not None:
            where_clauses.append("rating >= ?")
            params.append(min_rating)

        where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        # Total count
        cursor.execute(f"SELECT COUNT(*) FROM books{where_sql}", params)
        total = cursor.fetchone()[0]

        # Sorting
        order_sql = ""
        if sort_by == "price_asc":
            order_sql = " ORDER BY price ASC"
        elif sort_by == "price_desc":
            order_sql = " ORDER BY price DESC"
        elif sort_by == "rating_desc":
            order_sql = " ORDER BY rating DESC"

        # Pagination
        offset = (page - 1) * limit
        query = f"SELECT id, title, price, rating, image_url, product_url FROM books{where_sql}{order_sql} LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return total, rows

    def search_books(
        self, query_str: str, page: int = 1, limit: int = 20
    ) -> Tuple[int, List[Dict]]:
        conn = self._get_connection()
        cursor = conn.cursor()

        search_term = f"%{query_str}%"
        cursor.execute("SELECT COUNT(*) FROM books WHERE title LIKE ?", (search_term,))
        total = cursor.fetchone()[0]

        offset = (page - 1) * limit
        cursor.execute(
            "SELECT id, title, price, rating, image_url, product_url FROM books WHERE title LIKE ? LIMIT ? OFFSET ?",
            (search_term, limit, offset),
        )
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return total, rows

    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, price, rating, image_url, product_url FROM books WHERE id = ?",
            (book_id,),
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_stats(self) -> Dict:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*), AVG(price) FROM books")
        total, avg_price = cursor.fetchone()
        avg_price = round(avg_price, 2) if avg_price else 0.0

        cursor.execute("SELECT rating, COUNT(*) FROM books GROUP BY rating")
        rating_dist = {row[0]: row[1] for row in cursor.fetchall()}

        conn.close()
        return {
            "total_books": total,
            "average_price": avg_price,
            "rating_distribution": rating_dist,
        }

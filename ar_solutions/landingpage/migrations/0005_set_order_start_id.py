# Generated migration to start Order ID from 1001

from django.db import migrations


def set_order_start_sequence(apps, schema_editor):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        if connection.vendor == 'sqlite':
            cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='landingpage_order'")
            row = cursor.fetchone()
            if row:
                if row[0] < 1000:
                    cursor.execute("UPDATE sqlite_sequence SET seq=1000 WHERE name='landingpage_order'")
            else:
                cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('landingpage_order', 1000)")
        elif connection.vendor == 'postgresql':
            cursor.execute("SELECT setval(pg_get_serial_sequence('landingpage_order', 'id'), 1000, true);")
        elif connection.vendor == 'mysql':
            cursor.execute("ALTER TABLE landingpage_order AUTO_INCREMENT = 1001;")


class Migration(migrations.Migration):

    dependencies = [
        ('landingpage', '0004_product_badge_product_highlights_product_rating_and_more'),
    ]

    operations = [
        migrations.RunPython(set_order_start_sequence, reverse_code=migrations.RunPython.noop),
    ]


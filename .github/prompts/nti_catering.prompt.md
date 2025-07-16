---
mode: agent
---
Define the task to achieve, including specific requirements, constraints, and success criteria. I preferably use best practices and conventions in Odoo development, make it clean extend or even better maintainable, and scalable. Each complicated task should be broken down into smaller task, where you may feel like beginner is writting the code. Use best practices but dont overkill where it might too complicated for beginner to understand. Use Odoo 18, where tree is become list, and chatter simplified via tag chatter only.

---- 

for comment rules, you must use bahasa indonesia, and use the following format:
- non capitl for all of the comment
- use bahasa indonesia
- use this format

example:
" # method untuk mengubah state agar menjadi 'submitted' "
" # generate auto sesuai req, namun karena X dibutuhkan, maka dilakukan Y"

Module: nti_meal_catering

# Masalah User:
    1. Karyawan terakhir yang datang ke kantin terkadang tidak dapat makanan
    2. Makanan di akhir terkadang juga banyak yang tidak habis
    3. Karyawan tidak mengetahui jadwal makanan


# Keinginan case Users:
    1. Karyawan dapat melihat jadwal makanan per tiap pekan
    2. Karyawan dapat mengetahui apakah makanan masih tersedia atau tidak (dapat diupdate oleh koki)
    3. Karyawan dapat melakukan pemesanan makanan
    4. Karyawan dapat melakukan absensi makanan
    5. Notifikasi karyawan untuk melakukan pemesanan makanan
    6. chef dapat melihat jumlah pesanan makanan
    7. Admin dapat melakaukan pemetaan makanan, dengan menghitung jumlah karywan yang biasa hadir pada hari tersebut
    8. Pemetaan makanan oleh admin dapat menjadi dokumen purchase

# Gambaran Proses yang Diinginkan
    1. Admin menetapkan menu untuk minggu depan
    2. Karyawan memilih (konfirmasi) apakah mereka ingin makan di tanggal/menu tertentu
    3. Setelah batas waktu pemesanan, sistem otomatis:
        1. Merangkum jumlah bahan makanan yang dibutuhkan
        2. Menghitung total kebutuhan bahan baku berdasarkan pesanan
        3. Menghasilkan Request for Quotation (RFQ) atau Purchase Order (PO) di modul Purchase

# Notes Tasks:
   Akses base CRUD:
        user => hanya read saja aksesnya
        officer => dapat akses menu
        manager => dapat akses update
        admin => dapat akses create
        buat hierarchy groupsnya menggunakan implied_ids

# Task Requirement:

## 1. meal.order
    Model: meal.order
    view: kanban, form, tree, search
    security: 
        - Buat root category akses 'Meal'
        - Buat sub category akses 'Meal Order'
        - Buat base user akses CRUD dengan category Meal Order

        - Buat root category akses 'Meal'
        - Buat sub category akses 'Meal Order Advance'

        - Buat sub category akses 'Meal Order Advance' => parent ke Category 'Meal'
        - buat groups akses untuk tiap button dengan category Meal Order Advance
            - contoh groups nya 'Action Submit Meal Order' 
            - buat groups baru untuk setiap record rules yang dibutuhkan
                - record rules => full access
                - record rules => hanya boleh melihat responsible_id sesuai dengan user yang aktif
                - record rules => hanya boleh melihat chef_id sesuai dengan employee yang aktif
    fields:
        - name = sequence = MO/25/06/Sequence nya (Triggered saat di submit, default /)
        - chef_id(hr.employee, string Default 'Chef')
        - responsible_id(res.users) default dari user yang sedang aktif
        - date_from default mengambil tanggal di hari Senin di pekan depan
        - date_to default mengambil tanggal di hari Jumat di pekan depan
        - state['draft', 'submitted', 'on_going', 'done', 'canceled', 'rejected']
        - basic_quantity_user(integer)
        - actual_quantity_user(integer) compute ambil dari all_participant_ids
        - budget(monetary)
        - currency_id(res.currency)
        - meal_schedule_ids(meal.schedule)(o2m) default terbuat Senin - Jumat dengan date 
        - total_expense(monetary) compute ngambil total_price dari meal_schedule_ids.purchase_ids
        - purchase_count(integer) compute ngambil jumlah meal_schedule_ids.purchase_ids

        - participant_count(integer) compute ngambil jumlah all_participant_ids
        - internal_participant_ids(res.partner)
        - external_participant_ids(res.partner)
        - all_participant_ids(res.partner)
    
    function:
        - funcion perubahan state, muncul sesuai hirarki approval
            - action_submit => state 'submitted'
            - action_confirm => state 'on_going'
            - action_done => state 'done'
            - action_cancel => state 'canceled'
            - action_reject => state 'rejected'
        - function create purchase order (function ini akan dipanggil di funtion action_confirm())
            - purchase order akan di create sesuai dengan jumlah hari yang ada di meal_schedule_line_ids
            - akan mengisi purchase_ids juga di meal.schedule

## 2. meal.schedule
    view: kanban, calendar, form, tree, search
    security: 
        - Buat root category akses 'Meal'
        - Buat sub category akses 'Meal Schedule'
        - Buat base user akses CRUD dengan category Meal Schedule
    fields:
        - days(selection[1 = Sunday, 2 = Monday, 3 = Tuesday, 4 = Wednesday, 5 = Thursday, 6 = Friday, 7 = Saturday]) onchange dari date
        - date
        - time_from(float_time)
        - time_to(float_time)
        - user_quantity
        - adjustment_meal_quantity
        - meal_quantity (compute ngambil user_quantity + adjustment_meal_quantity)
        - meal_time[morning,lunch,diner]
        - status['open', 'closed']
        - meal_order_id(meal.order)
        
        - (gajadi) actual_meal_quantity compute ngambil jumlah meal_order
        - (gajadi) actual_user_quantity compute ngambil jumlah meal_preorder_ids
        - meal_preorder_line_ids(meal.preorder) o2m

        - internal_participant_ids(res.partner)
        - external_participant_ids(res.partner)
        - all_participant_ids(res.partner)
        - present_participant_ids(res.partner)
    view kanban:
        - Kreasikan sebaik mungkin
    view calendar:
        - acuan date nya menggunakan date, time_from, time_to

## 3. meal.schedule.line

        - product_id(product.product, string='Menu') => sebagai menu makanannya
        - product_category_id(product.category, string='Menu Category') => Lauk/Buah/Sayur, related=product_id.categ_id
        - bom_id(mrp.bom) => default keisi dari salah satu bom_ids di product, dikasih domain juga yang tampil hanya yang ada di bom_ids dalam product
        - quantity
        - schedule_id(meal.schedule)

    Security mengikuti meal.schedule

## 4. meal.preorder
    view: tree, search
    security: 
        - Buat sub category akses 'Meal Preorder'
        - Buat base user akses CRUD dengan category Meal Preorder
    fields:
        - meal_order_id(meal.order)
        - meal_schedule_id(meal.schedule)
        - date (related= meal_schedule.id.date)
        - participant_id(res.partner)
        - employee_id(hr.employee)
        - attend_status['absent', 'present','subtitute', 'late_present']
        - attend_type['dine_in', 'take_away ']
        - attend_time(float_time)
        - attend_datetime(onchange now saat ada perubahan attend status)
        - barcode(string)
        - substitute_id(res.partner) => maksimal 3x hanya untuk tiap meal_order_id

## 5. meal.substitute
    view: tree, search
    security: 
        - Buat sub category akses 'Meal Substitute'
        - Buat base user akses CRUD dengan category Meal Substitute
    fields:
        - meal_order_id(meal.order)
        - meal_schedule_id(meal.schedule)
        - date (related= meal_schedule.id.date)
        - participant_id(res.partner)
        - attend_type['dine_in', 'take_away']
        - attend_time(float_time)
        - attend_datetime(onchange now saat ada perubahan attend status)
        - barcode(string)
        - substitute_id(res.partner) => maksimal 3x hanya untuk tiap meal_order_id
    ketentuan:
    Kitchen akan scan barcode


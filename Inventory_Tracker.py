from tkinter import *
from tkinter import ttk
import sqlite3
import requests
from datetime import datetime
from usps import USPSApi
import json

# API Key
UPS_API_KEY = "4D7F42FDE3B9E45D"
usps = USPSApi("418NEDNY3865")


# Allows for frame cycling
def raise_frame(frame):
    frame.tkraise()


master = Tk()
master.geometry("1200x800")
master.title("Inventory Tracker")
options = ["Current", "Archived", "UPS Tracking", "USPS Tracking"]
master.state('zoomed')

# Creates all necessary frames
main_screen = Frame(master)
current_inventory = Frame(master)
current_add = Frame(master)
editor_current = Frame(master)
editor_archived = Frame(master)
archived_inventory = Frame(master)
archived_add = Frame(master)
ups_main = Frame(master)
ups_edit = Frame(master)
ups_add = Frame(master)
usps_main = Frame(master)
usps_edit = Frame(master)
usps_add = Frame(master)

for frame in (
        main_screen, current_inventory, current_add, editor_current, editor_archived, archived_inventory, archived_add,
        ups_main, ups_edit, ups_add, usps_main, usps_edit, usps_add):
    frame.grid(row=0, column=0, sticky='news')


# Stores input from current add item
def store_result_current():
    global current_result1
    global current_result2
    global current_result3
    global current_result4
    global current_result5
    global current_result6
    global current_result7
    global current_result8
    global current_result9
    global profit

    current_result1 = current_purchased_from.get()
    current_result2 = current_item_name.get()
    current_result3 = current_item_price.get()
    current_result4 = current_item_size.get()
    current_result5 = current_item_color.get()
    current_result6 = current_item_quantity.get()
    current_result7 = current_item_purchase_date.get()
    current_result8 = current_item_sold_date.get()
    current_result9 = current_item_sold_price.get()
    try:
        current_result3 = round(float(current_result3),2)
        current_result6 = int(current_result6)
        current_result9 = round(float(current_result9),2)
        profit = round((current_result9 - current_result3), 2)
        if len(current_result1) == 0 or len(current_result2) == 0 or current_result3 < 0 or current_result6 != 1 or current_result9 < 0 or len(current_result7) == 0:
            missing_field = Label(current_add_new_item,
                                  text="Check all that required fields are filled in properly.")
            missing_field.grid(row=10, column=1, padx=5, pady=5)
            current_add_new_item.after(3000, missing_field.destroy)
        else:
            if current_result9 == 0 and len(current_result8) == 0:
                raise_frame(current_inventory)
                connection = sqlite3.connect("Inventory.db")

                c = connection.cursor()
                c.execute(
                    "INSERT INTO Current_Inventory (rowid, purchased_from, item, price, size, color, quantity, purchase_date, sold_date, sold_price, profit) VALUES (NULL, :purchased_from, :item_name, :item_price, :item_size, :item_color, :item_quantity, :item_purchase_date, :item_sold_date, :item_sold_price, :profit)",
                    {"purchased_from": current_purchased_from.get().title(),
                     "item_name": current_item_name.get().title(),
                     "item_price": current_result3,
                     "item_size": current_item_size.get().title(),
                     "item_color": current_item_color.get().title(),
                     "item_quantity": current_item_quantity.get(),
                     "item_purchase_date": current_item_purchase_date.get(),
                     "item_sold_date" : current_item_sold_date.get(),
                     "item_sold_price": current_result9,
                     "profit": str(profit)})

                connection.commit()

                connection.close()

                display_current()

                current_purchased_from.delete(0, END)
                current_item_name.delete(0, END)
                current_item_price.delete(0, END)
                current_item_size.delete(0, END)
                current_item_color.delete(0, END)
                current_item_quantity.delete(0, END)
                current_item_purchase_date.delete(0, END)
                current_item_sold_date.delete(0, END)
                search_entry_current.delete(0, END)
                current_purchased_from.focus()

            else:

                raise_frame(current_inventory)
                connection = sqlite3.connect("Inventory.db")

                c = connection.cursor()

                c.execute(
                    "INSERT INTO Archived_Inventory (rowid, purchased_from, item, price, size, color, quantity, purchase_date, sold_date, sold_price, profit) VALUES (NULL, :purchased_from, :item_name, :item_price, :item_size, :item_color, :item_quantity, :item_purchase_date, :item_sold_date, :item_sold_price, :profit)",
                    {"purchased_from": current_purchased_from.get().title(),
                     "item_name": current_item_name.get().title(),
                     "item_price": current_result3,
                     "item_size": current_item_size.get().title(),
                     "item_color": current_item_color.get().title(),
                     "item_quantity": current_item_quantity.get(),
                     "item_purchase_date": current_item_purchase_date.get(),
                     "item_sold_date": current_item_sold_date.get(),
                     "item_sold_price": current_result9,
                     "profit": str(profit)})

                connection.commit()

                connection.close()

                display_current()

                current_purchased_from.delete(0, END)
                current_item_name.delete(0, END)
                current_item_price.delete(0, END)
                current_item_size.delete(0, END)
                current_item_color.delete(0, END)
                current_item_quantity.delete(0, END)
                current_item_purchase_date.delete(0, END)
                current_item_sold_date.delete(0, END)
                current_item_sold_price.delete(0, END)
                current_item_sold_price.insert(END, "0" )
                search_entry_current.delete(0, END)
                current_purchased_from.focus()

    except ValueError:
        value_error = Label(current_add_new_item,
                            text="Check all that required fields are filled in properly.")
        value_error.grid(row=10, column=1, padx=5, pady=5)
        current_add_new_item.after(3000, value_error.destroy)


# Stores input from archive add item
def store_result_archived():
    global archived_result1
    global archived_result2
    global archived_result3
    global archived_result4
    global archived_result5
    global archived_result6
    global archived_result7
    global archived_result8
    global archived_result9
    archived_result1 = archived_purchased_from.get()
    archived_result2 = archived_item_name.get()
    archived_result3 = archived_item_price.get()
    archived_result4 = archived_item_size.get()
    archived_result5 = archived_item_color.get()
    archived_result6 = archived_item_quantity.get()
    archived_result7 = archived_item_purchase_date.get()
    archived_result8 = archived_item_sold_date.get()
    archived_result9 = archived_item_sold_price.get()
    try:
        archived_result3 = round(float(archived_result3),2)
        archived_result6 = int(archived_result6)
        archived_result9 = round(float(archived_result9),2)
        profit = round((archived_result9 - archived_result3), 2)
        if len(archived_result1) == 0 or len(archived_result2) == 0 or archived_result3 < 0 or archived_result6 < 0 or archived_result9 <= 0 or len(archived_result8) == 0 or len(archived_result7) == 0:
            missing_field = Label(archived_add_new_item,
                                  text="Check all that required fields are filled in properly.")
            missing_field.grid(row=10, column=1, padx=5, pady=5)
            archived_add_new_item.after(3000, missing_field.destroy)
        else:
            raise_frame(archived_inventory)
            connection = sqlite3.connect("Inventory.db")

            c = connection.cursor()

            c.execute(
                "INSERT INTO Archived_Inventory VALUES (:purchased_from, :item_name, :item_price, :item_size, :item_color, :item_quantity, :item_purchase_date, :item_sold_date, :item_sold_price, :profit)",
                {"purchased_from": archived_purchased_from.get().title(),
                 "item_name": archived_item_name.get().title(),
                 "item_price": archived_result3,
                 "item_size": archived_item_size.get().title(),
                 "item_color": archived_item_color.get().title(),
                 "item_quantity": archived_item_quantity.get(),
                 "item_purchase_date": archived_item_purchase_date.get(),
                 "item_sold_date" :archived_item_sold_date.get(),
                 "item_sold_price": archived_result9,
                 "profit": str(profit)})

            connection.commit()

            connection.close()

            display_archived()

            archived_purchased_from.delete(0, END)
            archived_item_name.delete(0, END)
            archived_item_price.delete(0, END)
            archived_item_size.delete(0, END)
            archived_item_color.delete(0, END)
            archived_item_quantity.delete(0, END)
            archived_item_purchase_date.delete(0, END)
            archived_item_sold_date.delete(0, END)
            archived_item_sold_price.delete(0, END)
            archived_item_sold_price.insert(END, "0")
            search_entry_archived.delete(0, END)
            archived_purchased_from.focus()
    except ValueError:
        value_error = Label(archived_add_new_item, text="Check all that required fields are filled in properly.")
        value_error.grid(row=10, column=1, padx=5, pady=5)
        archived_add_new_item.after(3000, value_error.destroy)


def store_ups_tracking_number():
    if len(ups_tracking_number_entry.get()) == 18:
        connection = sqlite3.connect("Inventory.db")
        c = connection.cursor()

        c.execute("INSERT INTO UPS (tracking_number,purchased_from) VALUES (:tracking_number_entry, :shipper_entry)", {"tracking_number_entry": ups_tracking_number_entry.get().title(), "shipper_entry": ups_shipper_entry.get().title()})

        connection.commit()

        connection.close()

        ups_tracking_number_entry.delete(0, END)
        ups_shipper_entry.delete(0, END)
        search_entry_ups.delete(0, END)
        ups_tracking_number_entry.focus()

        raise_frame(ups_main)
        display_ups()
    else:
        check_again = Label(ups_tracking_add_new_item, text="Check tracking number again.")
        check_again.grid(row=8, column=1, pady=10)
        ups_tracking_add_new_item.after(3000, check_again.destroy)


def store_usps_tracking_number():
        connection = sqlite3.connect("Inventory.db")
        c = connection.cursor()

        c.execute("INSERT INTO USPS (tracking_number,purchased_from) VALUES (:tracking_number_entry, :shipper_entry)", {"tracking_number_entry": usps_tracking_number_entry.get().title(), "shipper_entry": usps_shipper_entry.get().title()})

        connection.commit()

        connection.close()

        usps_tracking_number_entry.delete(0, END)
        usps_shipper_entry.delete(0, END)
        search_entry_usps.delete(0, END)
        usps_tracking_number_entry.focus()

        raise_frame(usps_main)
        display_usps()


# Determines dropdown choice and creates table for respective choice
def selected(choice):
    if drop_down.get() == "Current":
        display_current()


    elif drop_down.get() == "Archived":
        display_archived()

    elif drop_down.get() == "UPS Tracking":
        connection = sqlite3.connect("Inventory.db")
        c = connection.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS UPS (Tracking_Number TEXT, Purchased_From TEXT, Status TEXT, Location TEXT, Date_Time TEXT)")
        raise_frame(ups_main)
        display_ups()

        connection.commit()
        connection.close()

    else:
        connection = sqlite3.connect("Inventory.db")
        c = connection.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS USPS (Tracking_Number TEXT, Purchased_From TEXT, Status TEXT, Location TEXT, Date_Time TEXT)")
        raise_frame(usps_main)
        display_usps()

        connection.commit()
        connection.close()


# Edits current inventory
def edit_current():
    raise_frame(editor_current)

    connection = sqlite3.connect("Inventory.db")

    c = connection.cursor()
    try:
        c.execute("SELECT * FROM Current_Inventory WHERE rowid=?", (current_record_table.item(current_selected_item)["values"][0],))

        current_purchased_from_editor.insert(0, current_record_table.item(current_selected_item)["values"][1])
        current_item_name_editor.insert(0, current_record_table.item(current_selected_item)["values"][2])
        current_item_price_editor.insert(0, current_record_table.item(current_selected_item)["values"][3])
        current_item_size_editor.insert(0, current_record_table.item(current_selected_item)["values"][4])
        current_item_color_editor.insert(0, current_record_table.item(current_selected_item)["values"][5])
        current_item_quantity_editor.insert(0, current_record_table.item(current_selected_item)["values"][6])
        current_item_purchase_date_editor.insert(0, current_record_table.item(current_selected_item)["values"][7])
        current_item_sold_date_editor.insert(0, current_record_table.item(current_selected_item)["values"][8])
        current_item_sold_price_editor.insert(0, current_record_table.item(current_selected_item)["values"][9])


        connection.commit()

        connection.close()
    except Exception as e:
        display_current()

# Edits archived inventory
def edit_archived():
    raise_frame(editor_archived)

    connection = sqlite3.connect("Inventory.db")

    c = connection.cursor()
    try:
        c.execute("SELECT * FROM Archived_Inventory WHERE rowid=?", (archived_record_table.item(archived_selected_item)["values"][0],))

        archived_purchased_from_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][1])
        archived_item_name_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][2])
        archived_item_price_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][3])
        archived_item_size_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][4])
        archived_item_color_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][5])
        archived_item_quantity_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][6])
        archived_item_purchase_date_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][7])
        archived_item_sold_date_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][8])
        archived_item_sold_price_editor.insert(0, archived_record_table.item(archived_selected_item)["values"][9])

        connection.commit()

        connection.close()

    except Exception as e:
       display_archived()

# Edits UPS tracking number
def edit_ups():
    raise_frame(ups_edit)
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    try:
        c.execute("SELECT * FROM UPS WHERE rowid =?", (ups_record_table.item(ups_selected_item)["values"][0],))

        ups_tracking_entry.insert(0, ups_record_table.item(ups_selected_item)["values"][1])
        ups_shipper_entry_editor.insert(0, ups_record_table.item(ups_selected_item)["values"][2])

        connection.commit()
        connection.close()
    except Exception as e:
        raise_frame(ups_main)
        display_ups()

# Edits USPS tracking number
def edit_usps():
    raise_frame(usps_edit)
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    try:
        c.execute("SELECT * FROM USPS WHERE rowid =?", (usps_record_table.item(usps_selected_item)["values"][0],))

        usps_tracking_entry.insert(0, usps_record_table.item(usps_selected_item)["values"][1])
        usps_shipper_entry_editor.insert(0, usps_record_table.item(usps_selected_item)["values"][2])

        connection.commit()
        connection.close()
    except Exception as e:
        raise_frame(usps_main)
        display_usps()


# Updates current inventory
def update_current():
    update_current_result3 = current_item_price_editor.get()
    update_current_result8 = current_item_sold_date_editor.get()
    update_current_result9 = current_item_sold_price_editor.get()
    update_current_result3 = round(float(update_current_result3), 2)
    update_current_result9 = round(float(update_current_result9), 2)
    update_profit = round(update_current_result9 - update_current_result3, 2)
    if update_current_result3 < 0 or update_current_result9 < 0:
        missing_field = Label(current_edit_frame,
                              text="Check all that required fields are filled in properly.")
        missing_field.grid(row=10, column=1, padx=5, pady=5)
        current_add_new_item.after(3000, missing_field.destroy)
    else:
        if update_current_result9 > 0 or len(update_current_result8) != 0:
            connection = sqlite3.connect("Inventory.db")

            c = connection.cursor()
            c.execute("DELETE FROM Current_Inventory WHERE rowid=?", (current_record_table.item(current_selected_item)["values"][0],))

            c.execute(
                "INSERT INTO Archived_Inventory (rowid, purchased_from, item, price, size, color, quantity, purchase_date, sold_date, sold_price, profit) VALUES (NULL, :purchased_from, :item_name, :item_price, :item_size, :item_color, :item_quantity, :item_purchase_date, :item_sold_date, :item_sold_price, :profit)",
                {"purchased_from": current_purchased_from_editor.get().title(),
                 "item_name": current_item_name_editor.get().title(),
                 "item_price": update_current_result3,
                 "item_size": current_item_size_editor.get().title(),
                 "item_color": current_item_color_editor.get().title(),
                 "item_quantity": current_item_quantity_editor.get(),
                 "item_purchase_date": current_item_purchase_date_editor.get(),
                 "item_sold_date" : current_item_sold_date_editor.get(),
                 "item_sold_price": update_current_result9,
                 "profit": str(update_profit)})

            connection.commit()

            connection.close()

            display_current()

            current_purchased_from_editor.delete(0, END)
            current_item_name_editor.delete(0, END)
            current_item_price_editor.delete(0, END)
            current_item_size_editor.delete(0, END)
            current_item_color_editor.delete(0, END)
            current_item_quantity_editor.delete(0, END)
            current_item_purchase_date_editor.delete(0, END)
            current_item_sold_date_editor.delete(0, END)
            current_item_sold_price_editor.delete(0, END)
            current_purchased_from_editor.focus()
            search_entry_current.delete(0, END)
        else:
            connection = sqlite3.connect("Inventory.db")

            c = connection.cursor()
            c.execute('''UPDATE Current_Inventory SET purchased_from =?, item =?, price =?, size =?, color=?, quantity =?, purchase_date =?, sold_date =?, sold_price =?, profit =? WHERE rowid=? ''',
                      (current_purchased_from_editor.get().title(), current_item_name_editor.get().title(), update_current_result3,
                       current_item_size_editor.get().title(), current_item_color_editor.get().title(), current_item_quantity_editor.get(), current_item_purchase_date_editor.get(),
                       current_item_sold_date_editor.get(), update_current_result9, str(update_profit), current_record_table.item(current_selected_item)["values"][0]))

            connection.commit()

            connection.close()

            display_current()

            current_purchased_from_editor.delete(0, END)
            current_item_name_editor.delete(0, END)
            current_item_price_editor.delete(0, END)
            current_item_size_editor.delete(0, END)
            current_item_color_editor.delete(0, END)
            current_item_quantity_editor.delete(0, END)
            current_item_purchase_date_editor.delete(0, END)
            current_item_sold_date_editor.delete(0, END)
            current_item_sold_price_editor.delete(0, END)
            current_purchased_from_editor.focus()
            search_entry_current.delete(0, END)


def update_archived():
        update_archived_result3 = archived_item_price_editor.get()
        update_archived_result9 = archived_item_sold_price_editor.get()
        update_archived_result3 = round(float(update_archived_result3), 2)
        update_archived_result9 = round(float(update_archived_result9), 2)
        update_archived_profit = round(update_archived_result9 - update_archived_result3, 2)
        if update_archived_result3 < 0 or update_archived_result9 <= 0:
            missing_field = Label(archived_edit_frame,
                                  text="Check all that required fields are filled in properly.")
            missing_field.grid(row=10, column=1, padx=5, pady=5)
            archived_add_new_item.after(3000, missing_field.destroy)
        else:

            connection = sqlite3.connect("Inventory.db")

            c = connection.cursor()
            c.execute(
                '''UPDATE Archived_Inventory SET purchased_from =?, item =?, price =?, size =?, color=?, quantity =?, purchase_date =?, sold_date =?, sold_price =?, profit =? WHERE rowid=? ''',
                (archived_purchased_from_editor.get().title(), archived_item_name_editor.get().title(),
                 update_archived_result3,
                 archived_item_size_editor.get().title(),
                 archived_item_color_editor.get().title(),
                 archived_item_quantity_editor.get(),
                 archived_item_purchase_date_editor.get(),
                 archived_item_sold_date_editor.get(),
                 update_archived_result9,
                 str(update_archived_profit),
                 archived_record_table.item(archived_selected_item)["values"][0]))

            connection.commit()

            connection.close()

            display_archived()

            archived_purchased_from_editor.delete(0, END)
            archived_item_name_editor.delete(0, END)
            archived_item_price_editor.delete(0, END)
            archived_item_size_editor.delete(0, END)
            archived_item_color_editor.delete(0, END)
            archived_item_quantity_editor.delete(0, END)
            archived_item_purchase_date_editor.delete(0, END)
            archived_item_sold_date_editor.delete(0, END)
            archived_item_sold_price_editor.delete(0, END)
            archived_purchased_from_editor.focus()
            search_entry_archived.delete(0, END)


def update_ups():
    if len(ups_tracking_entry.get()) == 18:
        connection = sqlite3.connect("Inventory.db")

        c = connection.cursor()

        c.execute(
            '''UPDATE UPS SET tracking_number =?, purchased_from =? WHERE rowid=? ''',
            (ups_tracking_entry.get().title(), ups_shipper_entry_editor.get().title(), ups_record_table.item(ups_selected_item)["values"][0]))

        connection.commit()

        connection.close()

        raise_frame(ups_main)
        display_ups()

        ups_tracking_entry.delete(0, END)
        ups_shipper_entry_editor.delete(0, END)
        ups_tracking_entry.focus()
        search_entry_ups.delete(0, END)
    else:
        check_again = Label(edit_ups_frame, text = "Check tracking number again.")
        check_again.grid(row=9, column=1, pady= 10)
        edit_ups_frame.after(3000, check_again.destroy)


def update_usps():
        connection = sqlite3.connect("Inventory.db")

        c = connection.cursor()

        c.execute(
            '''UPDATE USPS SET tracking_number =?, purchased_from =? WHERE rowid=? ''',
            (usps_tracking_entry.get().title(), usps_shipper_entry_editor.get().title(), usps_record_table.item(usps_selected_item)["values"][0]))

        connection.commit()

        connection.close()

        raise_frame(usps_main)
        display_usps()

        usps_tracking_entry.delete(0, END)
        usps_shipper_entry_editor.delete(0, END)
        usps_tracking_entry.focus()
        search_entry_usps.delete(0, END)


# Shows current inventory
current_item_count = StringVar()
current_item_count.set("Total items: 0")
def display_current():
    raise_frame(current_inventory)
    connection = sqlite3.connect("Inventory.db")

    c = connection.cursor()

    c.execute("SELECT ROWID, * FROM Current_Inventory ORDER BY purchased_from ASC, item ASC, size + 0 ASC")
    current_records = c.fetchall()
    for item in current_record_table.get_children():
        current_record_table.delete(item)

    for record in current_records:
        current_record_table.insert("", "end", values=record)

    current_item_count.set("Total items:" + " " + str(len(current_records)))

    connection.commit()

    connection.close()


# Shows archived inventory
archived_item_count = StringVar()
archived_item_count.set("Total items: 0")
def display_archived():
    raise_frame(archived_inventory)

    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    c.execute("SELECT ROWID, * FROM Archived_Inventory  ORDER BY purchased_from ASC, item ASC, size + 0 ASC")

    archived_records = c.fetchall()
    # Clear all records from the TreeView
    for item in archived_record_table.get_children():
        archived_record_table.delete(item)

    for record in archived_records:
        archived_record_table.insert("", "end", values=record)

    archived_item_count.set("Total items:" + " " + str(len(archived_records)))

    connection.commit()

    connection.close()


def display_ups():
    global ups_tracking_data
    global ups_status
    global ups_location
    global ups_time
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    c.execute("SELECT ROWID, * FROM UPS  ORDER BY purchased_from ASC")

    ups_records = c.fetchall()

    # Clear all records from the TreeView
    for item in ups_record_table.get_children():
        ups_record_table.delete(item)

    for record in ups_records:
        try:
            ups_tracking_data = get_ups_tracking_info(record[1])
            if "trackResponse" in ups_tracking_data:
                ups_package = ups_tracking_data["trackResponse"]["shipment"][0]["package"][0]["activity"][0]
                ups_status = ups_package["status"]["description"]
                ups_location = ups_package["location"]["address"]["city"].title() + ", " + ups_package["location"]["address"][
                    "stateProvince"]
                ups_time = datetime.strptime(ups_package["date"] + " " + ups_package["time"], "%Y%m%d  %H%M%S")
                ups_estimated_delivery_date = datetime.strptime(
                    ups_tracking_data["trackResponse"]["shipment"][0]["package"][0]["deliveryDate"][0]["date"], "%Y%m%d").date()
                if "deliveryDate" in ups_tracking_data["trackResponse"]["shipment"][0]["package"][0]:
                    ups_record_table.insert("", "end", values=(record[0], record[1], record[2], ups_status, ups_location, ups_time, ups_estimated_delivery_date))
            else:
                ups_record_table.insert("", "end", values=(record[0], record[1], record[2], "Check tracking number again."))
        except Exception as e:
            if "warnings" not in ups_tracking_data["trackResponse"]["shipment"][0]:
                ups_record_table.insert("", "end", values=(record[0], record[1], record[2], ups_status, ups_location, ups_time))
            else:
                ups_record_table.insert("", "end", values=(record[0], record[1], record[2], "Check tracking number again."))

    ups_main.after(300000, display_ups)

    connection.commit()
    connection.close()


def display_usps():
    global usps_status
    global usps_location
    global usps_time
    global usps_package
    global usps_estimated_delivery
    global usps_tracking_data
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    c.execute("SELECT ROWID, * FROM USPS  ORDER BY purchased_from ASC")

    usps_records = c.fetchall()

    # Clear all records from the TreeView
    for item in usps_record_table.get_children():
        usps_record_table.delete(item)

    for record in usps_records:
            try:
                usps_tracking_data = get_usps_tracking_info(record[1])
                if "TrackSummary" in usps_tracking_data["TrackResponse"]["TrackInfo"]:
                    usps_package = usps_tracking_data["TrackResponse"]["TrackInfo"]["TrackSummary"]
                    usps_status = usps_package["Event"]
                    usps_location = usps_package["EventCity"].title() + ", " + usps_package["EventState"]
                    usps_time = usps_package["EventDate"] + " " + usps_package["EventTime"]
                    if "Error" not in usps_tracking_data["TrackResponse"]["TrackInfo"] and "ExpectedDeliveryDate" in usps_tracking_data["TrackResponse"]["TrackInfo"]:
                        usps_estimated_delivery = usps_tracking_data["TrackResponse"]["TrackInfo"][
                            "ExpectedDeliveryDate"]
                        usps_record_table.insert("", "end", values = (record[0], record[1], record[2], usps_status, usps_location, usps_time, usps_estimated_delivery))
                    elif "Error" not in usps_tracking_data["TrackResponse"]["TrackInfo"] and "ExpectedDeliveryDate" not in usps_tracking_data["TrackResponse"]["TrackInfo"]:
                        usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, usps_location, usps_time, "Not Available"))
                    else:
                        usps_error = usps_tracking_data["TrackResponse"]["TrackInfo"]["Error"]["Description"]
                        usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_error))
                else:
                    usps_error = usps_tracking_data["TrackResponse"]["TrackInfo"]["Error"]["Description"]
                    usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_error))
            except Exception as e:
                if "ExpectDeliveryDate" in usps_tracking_data["TrackResponse"]["TrackInfo"]:
                    if usps_package["EventCity"] is None and usps_package["EventState"] is None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"] + " " + usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                    elif usps_package["EventCity"] is None and usps_package["EventState"] is not None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, usps_package["EventState"], usps_package["EventDate"] + " " + usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                    elif usps_package["EventCity"] is not None and usps_package["EventState"] is None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, usps_package["EventCity"].title(), usps_package["EventDate"] + " " + usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                else:
                    if usps_package["EventCity"] is None and usps_package["EventState"] is None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available",
                            usps_package["EventDate"] + " " + usps_package["EventTime"], "Not Available"))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], "Not Available"))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], "Not Available"))
                    elif usps_package["EventCity"] is None and usps_package["EventState"] is not None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, usps_package["EventState"],
                            usps_package["EventDate"] + " " + usps_package["EventTime"], "Not Available"))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], "Not Available"))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], "Not Available"))
                    elif usps_package["EventCity"] is not None and usps_package["EventState"] is None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, usps_package["EventCity"].title(),
                            usps_package["EventDate"] + " " + usps_package["EventTime"], "Not Available"))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], "Not Available"))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], "Not Available"))

    usps_main.after(300000, display_usps)

    connection.commit()
    connection.close()


total_label_startup = StringVar()
total_label_startup.set("Current Expenses: $0.00")
overall_profit_startup = StringVar()
overall_profit_startup.set("Lifetime Profit: $0.00")

def display_stats():
    global total_label
    global overall_profit_label
    global overall_expense_label
    global total_current_expense
    connection = sqlite3.connect("Inventory.db")

    c = connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Current_Inventory (Purchased_From TEXT, Item TEXT, Price REAL, Size TEXT, Color TEXT, Quantity INTEGER, Purchase_Date TEXT, Sold_Date TEXT, Sold_Price REAL, Profit REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS Archived_Inventory (Purchased_From TEXT, Item TEXT, Price REAL, Size TEXT, Color TEXT, Quantity INTEGER, Purchase_Date TEXT, Sold_Date TEXT, Sold_Price REAL, Profit REAL)")
    c.execute("SELECT * FROM Current_Inventory")
    number_of_current = c.fetchall()
    c.execute("SELECT * FROM Archived_Inventory")
    number_of_archived = c.fetchall()

    if len(number_of_current) != 0:
        c.execute("SELECT SUM(price) FROM Current_Inventory")
        total_current = c.fetchall()
        if total_current[0][0] is not None:
            total_current_expense = round(total_current[0][0], 2)

            total_label_startup.set("Current Expenses:" + " " + "$" + str(total_current_expense))
    else:
        total_label_startup.set("Current Expenses: $0.00")

    if len(number_of_archived) != 0:
        c.execute("SELECT SUM(profit) FROM Archived_Inventory")
        total_archived_profit = c.fetchall()
        if total_archived_profit[0][0] is not None:
            overall_profit = round(total_archived_profit[0][0],2)

            overall_profit_startup.set("Lifetime Profit:" + " " + "$" + str(overall_profit))
    else:
        overall_profit_startup.set("Lifetime Profit: $0.00")


    connection.commit()
    connection.close()
    raise_frame(main_screen)


def duplicate_current():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    try:
        for item in current_selected_item:
            c.execute("INSERT INTO Current_Inventory SELECT * FROM Current_Inventory WHERE ROWID = ?", (current_record_table.item(item)["values"][0],))

        connection.commit()
        connection.close()

        search_entry_current.delete(0, END)
        display_current()

    except Exception as e:
        display_current()


def duplicate_archived():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    try:
        for item in archived_selected_item:
            c.execute("INSERT INTO Archived_Inventory SELECT * FROM Archived_Inventory WHERE ROWID = ?",
                      (archived_record_table.item(item)["values"][0],))

        connection.commit()
        connection.close()

        search_entry_archived.delete(0, END)
        display_archived()

    except Exception as e:
        display_archived()


# Clears entry field when clicking current back button
def back_clear_current():
    display_current()
    current_purchased_from.delete(0, END)
    current_item_name.delete(0, END)
    current_item_price.delete(0, END)
    current_item_size.delete(0, END)
    current_item_color.delete(0, END)
    current_item_quantity.delete(0, END)
    current_item_purchase_date.delete(0, END)
    current_item_sold_date.delete(0, END)
    search_entry_current.delete(0, END)


# Clears entry field when clicking archived back button
def back_clear_archived():
    display_archived()
    archived_purchased_from.delete(0, END)
    archived_item_name.delete(0, END)
    archived_item_price.delete(0, END)
    archived_item_size.delete(0, END)
    archived_item_color.delete(0, END)
    archived_item_quantity.delete(0, END)
    archived_item_purchase_date.delete(0, END)
    archived_item_sold_date.delete(0, END)
    search_entry_archived.delete(0, END)


# Clear entry fields when clicking ups back button
def back_clear_ups():
    ups_tracking_number_entry.delete(0, END)
    ups_shipper_entry.delete(0, END)
    raise_frame(ups_main)
    display_ups()


def back_clear_usps():
    usps_tracking_number_entry.delete(0, END)
    usps_shipper_entry.delete(0, END)
    raise_frame(usps_main)
    display_usps()


# Back button function on editor current
def back_editor_current():
    current_purchased_from_editor.delete(0, END)
    current_item_name_editor.delete(0, END)
    current_item_price_editor.delete(0, END)
    current_item_size_editor.delete(0, END)
    current_item_color_editor.delete(0, END)
    current_item_quantity_editor.delete(0, END)
    current_item_purchase_date_editor.delete(0, END)
    current_item_sold_date_editor.delete(0, END)
    current_item_sold_price_editor.delete(0, END)
    search_entry_current.delete(0, END)
    display_current()


# Back button function on editor archived
def back_editor_archived():
    archived_purchased_from_editor.delete(0, END)
    archived_item_name_editor.delete(0, END)
    archived_item_price_editor.delete(0, END)
    archived_item_size_editor.delete(0, END)
    archived_item_color_editor.delete(0, END)
    archived_item_quantity_editor.delete(0, END)
    archived_item_purchase_date_editor.delete(0, END)
    archived_item_sold_date_editor.delete(0, END)
    archived_item_sold_price_editor.delete(0, END)
    search_entry_archived.delete(0, END)
    display_archived()


def back_editor_ups():
    ups_tracking_entry.delete(0, END)
    ups_shipper_entry_editor.delete(0, END)
    raise_frame(ups_main)
    display_ups()


def back_editor_usps():
    usps_tracking_entry.delete(0, END)
    usps_shipper_entry_editor.delete(0, END)
    raise_frame(usps_main)
    display_usps()


# Deletes selection current table
def delete_current():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    try:
        for item in current_selected_item:
            c.execute("DELETE FROM Current_Inventory WHERE rowid=?", (current_record_table.item(item)["values"][0],))
        connection.commit()
        connection.close()

        display_current()
        search_entry_current.delete(0, END)
    except Exception as e:
        display_current()


# Deletes selection archived table
def delete_archived():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    try:
        for item in archived_selected_item:
            c.execute("DELETE FROM Archived_Inventory WHERE rowid=?", (archived_record_table.item(item)["values"][0],))
        connection.commit()
        connection.close()

        display_archived()
        search_entry_archived.delete(0, END)
    except Exception as e:
        display_archived()

def delete_ups():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    try:
        for item in ups_selected_item:
            c.execute("DELETE FROM UPS WHERE rowid=?", (ups_record_table.item(item)["values"][0],))
        connection.commit()
        connection.close()

        display_ups()
        search_entry_ups.delete(0, END)
    except Exception as e:
        display_ups()


def delete_usps():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    try:
        for item in usps_selected_item:
            c.execute("DELETE FROM USPS WHERE rowid=?", (usps_record_table.item(item)["values"][0],))
        connection.commit()
        connection.close()

        display_usps()
        search_entry_usps.delete(0, END)
    except Exception as e:
        display_usps()


def select_item_current(selection):
    global current_selected_item
    current_selected_item = current_record_table.selection()


def select_item_archived(selection):
    global archived_selected_item
    archived_selected_item = archived_record_table.selection()



def select_item_ups(selection):
    global ups_selected_item
    ups_selected_item = ups_record_table.selection()


def select_item_usps(selection):
    global usps_selected_item
    usps_selected_item = usps_record_table.selection()


def get_ups_tracking_info(trackingNum):
    headers = {"AccessLicenseNumber": UPS_API_KEY}
    url = f"https://onlinetools.ups.com/track/v1/details/{trackingNum}?locale=en_US"
    resp = requests.get(url, headers=headers)
    return resp.json()

def get_usps_tracking_info(tracking_num):
    usps_tracking_status = usps.track(tracking_num).result
    return usps_tracking_status


def current_search():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    searched = search_entry_current.get().title()

    c.execute(
        "SELECT ROWID, * FROM Current_Inventory WHERE purchased_from =? OR item =? OR price =? OR size =? OR color =? OR purchase_date =? OR sold_date =? OR sold_price =? ORDER BY item ASC, size + 0 ASC",
        (searched, searched, searched, searched, searched, searched, searched, searched))
    current_search_records = c.fetchall()
    if len(searched) != 0:
        if len(current_search_records) != 0:
            for item in current_record_table.get_children():
                current_record_table.delete(item)

            for record in current_search_records:
                current_record_table.insert("", "end", values=record)
            current_item_count.set("Total items:" + " " + str(len(current_search_records)))

        else:
            for item in current_record_table.get_children():
                current_record_table.delete(item)

            current_record_table.insert("", "end",
                                        values=(
                                            "", "No items found", "No items found", "No items found",
                                            "No items found",
                                            "No items found", "No items found", "No items found", "No items found",
                                            "No items found", "No items found"))
            current_item_count.set("Total items: 0")

    current_record_table.yview_moveto(0)

    connection.commit()
    connection.close()


def current_clear_search():
    search_entry_current.delete(0, END)
    current_record_table.yview_moveto(0)
    display_current()


def archived_search():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    searched = search_entry_archived.get().title()

    c.execute(
        "SELECT ROWID, * FROM Archived_Inventory WHERE purchased_from =? OR item =? OR price =? OR size =? OR color =? OR purchase_date =? OR sold_date =? OR sold_price =? ORDER BY item ASC, size + 0 ASC",
        (searched, searched, searched, searched, searched, searched, searched, searched))
    archived_search_records = c.fetchall()
    if len(searched) != 0:
        if len(archived_search_records) != 0:
            for item in archived_record_table.get_children():
                archived_record_table.delete(item)

            for record in archived_search_records:
                archived_record_table.insert("", "end", values=record)
            archived_item_count.set("Total items:" + " " + str(len(archived_search_records)))

        else:
            for item in archived_record_table.get_children():
                archived_record_table.delete(item)

            archived_record_table.insert("", "end", values=("","No items found", "No items found", "No items found", "No items found",
                                                                "No items found", "No items found", "No items found", "No items found",
                                                            "No items found", "No items found"))
            archived_item_count.set("Total items: 0")

    archived_record_table.yview_moveto(0)

    connection.commit()
    connection.close()


def archived_clear_search():
    search_entry_archived.delete(0, END)
    archived_record_table.yview_moveto(0)
    display_archived()


def ups_search():
    global search_tracking_data
    global search_status
    global search_location
    global search_time
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    searched = search_entry_ups.get().title()
    c.execute("SELECT ROWID, * FROM UPS WHERE tracking_number =? OR purchased_from =?",
              (searched, searched))
    ups_search_records = c.fetchall()
    if len(searched) != 0:
        if len(ups_search_records) != 0:
            for item in ups_record_table.get_children():
                ups_record_table.delete(item)

            for record in ups_search_records:
                try:
                    search_tracking_data = get_ups_tracking_info(record[1])
                    if "trackResponse" in search_tracking_data:
                        search_package = search_tracking_data["trackResponse"]["shipment"][0]["package"][0]["activity"][0]
                        search_status = search_package["status"]["description"]
                        search_location = search_package["location"]["address"]["city"].title() + ", " + search_package["location"]["address"][
                            "stateProvince"]
                        search_time = datetime.strptime(search_package["date"] + " " + search_package["time"], "%Y%m%d  %H%M%S")
                        search_estimated_delivery_date = datetime.strptime(
                            search_tracking_data["trackResponse"]["shipment"][0]["package"][0]["deliveryDate"][0]["date"],
                            "%Y%m%d").date()
                        if "deliveryDate" in search_tracking_data["trackResponse"]["shipment"][0]["package"][0]:
                            ups_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], search_status, search_location, search_time, search_estimated_delivery_date))
                    else:
                        ups_record_table.insert("", "end",
                                                values=(record[0], record[1], record[2], "Check tracking number again."))
                except Exception as e:
                    if "warnings" not in search_tracking_data["trackResponse"]["shipment"][0]:
                        ups_record_table.insert("", "end", values=(record[0], record[1], record[2], search_status, search_location, search_time))
                    else:
                        ups_record_table.insert("", "end",
                                                values=(record[0], record[1], record[2], "Check tracking number again."))
        else:
            for item in ups_record_table.get_children():
                ups_record_table.delete(item)

            ups_record_table.insert("", "end", values=("", "No records found", "No records found", "No records found", "No records found", "No records found", "No records found"))

    ups_record_table.yview_moveto(0)

    connection.commit()
    connection.close()


def ups_clear_search():
    search_entry_ups.delete(0, END)
    ups_record_table.yview_moveto(0)
    display_ups()


def usps_search():
    connection = sqlite3.connect("Inventory.db")
    c = connection.cursor()
    searched = search_entry_usps.get().title()
    c.execute("SELECT ROWID, * FROM USPS WHERE tracking_number =? OR purchased_from =?",
              (searched, searched))
    usps_search_records = c.fetchall()
    if len(searched) != 0:
        if len(usps_search_records) != 0:
            for item in usps_record_table.get_children():
                usps_record_table.delete(item)

            for record in usps_search_records:
                try:
                    usps_tracking_data = get_usps_tracking_info(record[1])
                    print(usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"])
                    if "TrackSummary" in usps_tracking_data["TrackResponse"]["TrackInfo"]:
                        usps_package = usps_tracking_data["TrackResponse"]["TrackInfo"]["TrackSummary"]
                        usps_status = usps_package["Event"]
                        usps_location = usps_package["EventCity"].title() + ", " + usps_package["EventState"]
                        usps_time = usps_package["EventDate"] + " " + usps_package["EventTime"]
                        usps_estimated_delivery = usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]
                        if "Error" not in usps_tracking_data["TrackResponse"]["TrackInfo"]:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, usps_location, usps_time, usps_estimated_delivery))
                        else:
                            usps_error = usps_tracking_data["TrackResponse"]["TrackInfo"]["Error"]["Description"]
                            usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_error))
                    else:
                        usps_error = usps_tracking_data["TrackResponse"]["TrackInfo"]["Error"]["Description"]
                        usps_record_table.insert("", "end", values=(record[0], record[1], record[2], usps_error))
                except Exception as e:
                    if usps_package["EventCity"] is None and usps_package["EventState"] is None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available",
                            usps_package["EventDate"] + " " + usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                    elif usps_package["EventCity"] is None and usps_package["EventState"] is not None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, usps_package["EventState"],
                            usps_package["EventDate"] + " " + usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                    elif usps_package["EventCity"] is not None and usps_package["EventState"] is None:
                        if usps_package["EventTime"] is not None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, usps_package["EventCity"].title(),
                            usps_package["EventDate"] + " " + usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is None and usps_package["EventDate"] is not None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventDate"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))
                        elif usps_package["EventTime"] is not None and usps_package["EventDate"] is None:
                            usps_record_table.insert("", "end", values=(
                            record[0], record[1], record[2], usps_status, "Not Available", usps_package["EventTime"], usps_tracking_data["TrackResponse"]["TrackInfo"]["ExpectedDeliveryDate"]))

    usps_record_table.yview_moveto(0)

    connection.commit()
    connection.close()


def usps_clear_search():
    search_entry_usps.delete(0, END)
    usps_record_table.yview_moveto(0)
    display_usps()


def current_home_button():
    search_entry_current.delete(0, END)
    current_record_table.yview_moveto(0)
    display_stats()



def archived_home_button():
    search_entry_archived.delete(0, END)
    archived_record_table.yview_moveto(0)
    display_stats()


def ups_home_button():
    display_stats()

def usps_home_button():
    display_stats()


def current_treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, text=col, command=lambda _col=col: \
                 current_treeview_sort_column(tv, _col, not reverse))


def archived_treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, text=col, command=lambda _col=col: \
                 archived_treeview_sort_column(tv, _col, not reverse))


def ups_treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, text=col, command=lambda _col=col: \
                 ups_treeview_sort_column(tv, _col, not reverse))


def usps_treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, text=col, command=lambda _col=col: \
                 usps_treeview_sort_column(tv, _col, not reverse))





# def graph_current_expense():
#     connection = sqlite3.connect("Inventory.db")
#     c = connection.cursor()
#     c.execute("SELECT Price FROM Current_Inventory")
#
#     values = []
#     for row in c.fetchall():
#         values.append(row[0])
#
#     plt.hist(values)
#     plt.show()
#     connection.commit()
#     connection.close()


# def startup():
#     connection = sqlite3.connect("Inventory.db")
#     c = connection.cursor()
#     c.execute("UPDATE Current_Inventory SET purchased_from = dbo.fn_title_case(purchased_from), item = dbo.fn_title_case(item), price = dbo.fn_title_case(price),"
#               " size = dbo.fn_title_case(size), color = dbo.fn_title_case(color),quantity = dbo.fn_title_case(quantity), purchase_date = dbo.fn_title_case(purchase_date),"
#               " sold_date = dbo.fn_title_case(sold_date), sold_price = dbo.fn_title_case(sold_price), profit = dbo.fn_title_case(profit)")
#
#     connection.commit()
#     connection.close()



home_button_current_inventory = Button(current_inventory, text="Home", command=current_home_button,
                                       font="TkDefaultFont 9 bold").place(x=20, y=15)
home_button_archived_inventory = Button(archived_inventory, text="Home", command= archived_home_button,
                                        font="TkDefaultFont 9 bold").place(x=20, y=15)
home_button_ups = Button(ups_main, text="Home", command= ups_home_button,
                         font="TkDefaultFont 9 bold").place(x=20, y=15)
home_button_usps = Button(usps_main, text="Home", command= usps_home_button,
                         font="TkDefaultFont 9 bold").place(x=20, y=15)

back_button_current_add = Button(current_add, text="Back", command=back_clear_current,
                                 font="TkDefaultFont 9 bold").place(x=20, y=15)
back_button_archived_add = Button(archived_add, text="Back", command=back_clear_archived,
                                  font="TkDefaultFont 9 bold").place(x=20, y=15)
back_button_ups_add = Button(ups_add, text="Back", command=back_clear_ups,
                                  font="TkDefaultFont 9 bold").place(x=20, y=15)
back_button_usps_add = Button(usps_add, text="Back", command=back_clear_usps,
                                  font="TkDefaultFont 9 bold").place(x=20, y=15)

back_button_current_editor = Button(editor_current, text="Back", command=back_editor_current,
                                    font="TkDefaultFont 9 bold").place(x=20, y=15)
back_button_archived_editor = Button(editor_archived, text="Back", command=back_editor_archived,
                                     font="TkDefaultFont 9 bold").place(x=20, y=15)
back_button_ups_editor = Button(ups_edit, text="Back", command=back_editor_ups,
                                     font="TkDefaultFont 9 bold").place(x=20, y=15)
back_button_usps_editor = Button(usps_edit, text="Back", command=back_editor_usps,
                                     font="TkDefaultFont 9 bold").place(x=20, y=15)

add_button_current = Button(current_inventory, text="Add Item", command= lambda:raise_frame(current_add),
                            font="TkDefaultFont 9 bold").place(x=300, y=63)
add_button_archived = Button(archived_inventory, text="Add Item", command = lambda:raise_frame(archived_add),
                             font="TkDefaultFont 9 bold").place(x=300, y=63)
add_button_ups = Button(ups_main, text="Add Item", command=lambda: raise_frame(ups_add),
                        font="TkDefaultFont 9 bold").place(x=375, y=63)
add_button_usps = Button(usps_main, text="Add Item", command=lambda: raise_frame(usps_add),
                        font="TkDefaultFont 9 bold").place(x=375, y=63)

edit_button_current = Button(current_inventory, text="Edit Item", command=edit_current,
                             font="TkDefaultFont 9 bold").place(x=375, y=63)
edit_button_archived = Button(archived_inventory, text="Edit Item", command=edit_archived,
                              font="TkDefaultFont 9 bold").place(x=375, y=63)
edit_button_ups = Button(ups_main, text="Edit Item", command=edit_ups,
                         font="TkDefaultFont 9 bold").place(x=450, y=63)
edit_button_usps = Button(usps_main, text="Edit Item", command=edit_usps,
                         font="TkDefaultFont 9 bold").place(x=450, y=63)

delete_button_current = Button(current_inventory, text="Delete Item", font="TkDefaultFont 9 bold",
                               command=delete_current).place(x=450, y=63)
delete_button_archived = Button(archived_inventory, text="Delete Item", font="TkDefaultFont 9 bold",
                                command=delete_archived).place(x=450, y=63)
delete_button_ups = Button(ups_main, text="Delete Item", font="TkDefaultFont 9 bold",
                           command=delete_ups).place(x=525, y=63)
delete_button_usps = Button(usps_main, text="Delete Item", font="TkDefaultFont 9 bold",
                           command=delete_usps).place(x=525, y=63)

duplicate_button_current = Button(current_inventory, text = "Duplicate Item", font = "TkDefaultFont 9 bold", command = duplicate_current).place(x = 540, y= 63)
duplicate_button_archived = Button(archived_inventory, text = "Duplicate Item", font = "TkDefaultFont 9 bold", command = duplicate_archived).place(x = 540, y= 63)


search_button_current = Button(current_inventory, text = "Search", font = "TkDefaultFont 9 bold", command = current_search).place(x = 1655, y =63)
clear_button_current = Button(current_inventory, text = "Clear Search", font = "TkDefaultFont 9 bold", command = current_clear_search).place(x = 1720, y =63)
search_entry_current = Entry(current_inventory, justify = "center")
search_entry_current.place(x = 1510, y= 67)
search_entry_current_label = Label(current_inventory, text = "Item Lookup:", font = "TkDefaultFont 9 bold").place(x = 1425, y= 66)

search_button_archived = Button(archived_inventory, text = "Search", font = "TkDefaultFont 9 bold", command = archived_search).place(x = 1655, y =63)
clear_button_archived = Button(archived_inventory, text = "Clear Search", font = "TkDefaultFont 9 bold", command = archived_clear_search).place(x = 1720, y =63)
search_entry_archived = Entry(archived_inventory, justify = "center")
search_entry_archived.place(x = 1510, y= 67)
search_entry_archived_label = Label(archived_inventory, text = "Item Lookup:", font = "TkDefaultFont 9 bold").place(x = 1425, y= 66)

search_button_ups = Button(ups_main, text = "Search", font = "TkDefaultFont 9 bold", command = ups_search).place(x = 1525, y =63)
clear_button_ups = Button(ups_main, text = "Clear Search", font = "TkDefaultFont 9 bold", command = ups_clear_search).place(x = 1590, y =63)
search_entry_ups = Entry(ups_main, justify = "center")
search_entry_ups.place(x = 1390, y= 67)
search_entry_ups_label = Label(ups_main, text = "Item Lookup:", font = "TkDefaultFont 9 bold").place(x = 1305, y= 66)

search_button_usps = Button(usps_main, text = "Search", font = "TkDefaultFont 9 bold", command = usps_search).place(x = 1525, y =63)
clear_button_usps = Button(usps_main, text = "Clear Search", font = "TkDefaultFont 9 bold", command = usps_clear_search).place(x = 1590, y =63)
search_entry_usps = Entry(usps_main, justify = "center")
search_entry_usps.place(x = 1390, y= 67)
search_entry_usps_label = Label(usps_main, text = "Item Lookup:", font = "TkDefaultFont 9 bold").place(x = 1305, y= 66)


current_add_new_item = LabelFrame(current_add, text="Add Item", labelanchor="n", font="TkDefaultFont 12 bold")
current_add_new_item.grid(sticky="news", padx=775, pady=250)
archived_add_new_item = LabelFrame(archived_add, text="Add Item", labelanchor="n", font="TkDefaultFont 12 bold")
archived_add_new_item.grid(sticky="news", padx=775, pady=250)
ups_tracking_add_new_item = LabelFrame(ups_add, text = "Add Tracking", labelanchor = "n", font = "TkDefaultFont 12 bold")
ups_tracking_add_new_item.grid(sticky="news", padx=775, pady=400)
usps_tracking_add_new_item = LabelFrame(usps_add, text = "Add Tracking", labelanchor = "n", font = "TkDefaultFont 12 bold")
usps_tracking_add_new_item.grid(sticky="news", padx=775, pady=400)

manage_item = LabelFrame(main_screen, text="Manage Items", labelanchor="n", font="TkDefaultFont 12 bold")
manage_item.grid(sticky="news", padx=850, pady=550)

stats = LabelFrame(main_screen, text="Stats", labelanchor="n", font="TkDefaultFont 12 bold")
stats.place(relx=0.5, rely=0.30, anchor= CENTER)

edit_ups_frame = LabelFrame(ups_edit, text ="Edit Tracking", labelanchor ="n", font ="TkDefaultFont 12 bold")
edit_ups_frame.pack(pady = 400)

edit_usps_frame = LabelFrame(usps_edit, text ="Edit Tracking", labelanchor ="n", font ="TkDefaultFont 12 bold")
edit_usps_frame.pack(pady = 400)

archived_edit_frame = LabelFrame(editor_archived, text="Item Editor", padx=5, pady=5, labelanchor="n",
                        font="TkDefaultFont 12 bold")
archived_edit_frame.pack(pady=250)
current_edit_frame = LabelFrame(editor_current, text="Item Editor", padx=5, pady=5, labelanchor="n",
                        font="TkDefaultFont 12 bold")
current_edit_frame.pack(pady=250)

drop_down = ttk.Combobox(manage_item, value=options, justify="center")
drop_down.bind("<<ComboboxSelected>>", selected)
drop_down.pack(padx=30, pady=25)

current_submit = Button(current_add_new_item, text="Submit", command=store_result_current)
archived_submit = Button(archived_add_new_item, text="Submit", command=store_result_archived)
ups_submit = Button(ups_tracking_add_new_item, text="Submit", command=store_ups_tracking_number)
ups_submit.grid(row=7, column=1, padx=10, pady=10)
usps_submit = Button(usps_tracking_add_new_item, text="Submit", command=store_usps_tracking_number)
usps_submit.grid(row=7, column=1, padx=10, pady=10)
archived_save_button = Button(archived_edit_frame, text="Save Changes", command=update_archived)
archived_save_button.grid(row=9, column=1, pady = 10)
current_save_button = Button(current_edit_frame, text="Save Changes", command=update_current)
current_save_button.grid(row=9, column=1, pady = 10)




current_inventory_label = Label(current_inventory, text="Current Inventory", font="TkDefaultFont 12 bold").place(
    x=130, y=63)
archived_inventory_label = Label(archived_inventory, text="Archived Inventory", font="TkDefaultFont 12 bold").place(
    x=130, y=63)
ups_label = Label(ups_main, text="UPS Tracking", font="TkDefaultFont 12 bold").place(
    x=230, y=63)
usps_label = Label(usps_main, text="USPS Tracking", font="TkDefaultFont 12 bold").place(
    x=230, y=63)

# Entry boxes for current add item
current_purchased_from = Entry(current_add_new_item, justify="center")
current_item_name = Entry(current_add_new_item, justify="center")
current_item_price = Entry(current_add_new_item, justify="center")
current_item_size = Entry(current_add_new_item, justify="center")
current_item_color = Entry(current_add_new_item, justify= "center")
current_item_quantity = Entry(current_add_new_item, justify="center")
current_item_quantity.insert(END, "1")
current_item_quantity.config(state = DISABLED)
current_item_purchase_date = Entry(current_add_new_item, justify="center")
current_item_sold_date = Entry(current_add_new_item, justify= "center")
current_item_sold_price = Entry(current_add_new_item, justify="center")
current_item_sold_price.insert(END, "0")

# Entry boxes for archived add item
archived_purchased_from = Entry(archived_add_new_item, justify="center")
archived_item_name = Entry(archived_add_new_item, justify="center")
archived_item_price = Entry(archived_add_new_item, justify="center")
archived_item_size = Entry(archived_add_new_item, justify="center")
archived_item_color = Entry(archived_add_new_item, justify = "center")
archived_item_quantity = Entry(archived_add_new_item, justify="center")
archived_item_quantity.insert(END, "1")
archived_item_quantity.config(state = DISABLED)
archived_item_purchase_date = Entry(archived_add_new_item, justify="center")
archived_item_sold_date = Entry(archived_add_new_item, justify = "center")
archived_item_sold_price = Entry(archived_add_new_item, justify="center")
archived_item_sold_price.insert(END, "0")

archived_location_editor = Label(archived_edit_frame, text="*Where item was purchased from:")
archived_name_editor = Label(archived_edit_frame, text="*Item:")
archived_price_editor = Label(archived_edit_frame, text="*Price:")
archived_size_editor = Label(archived_edit_frame, text="Size:")
archived_color_editor = Label(archived_edit_frame, text = "Color/Style:")
archived_quantity_editor = Label(archived_edit_frame, text="Quantity:")
archived_purchase_date_editor = Label(archived_edit_frame, text="*Purchase Date (mm/dd/yyyy):")
archived_sold_date_editor = Label(archived_edit_frame, text = "*Sold Date (mm/dd/yyyy):")
archived_sold_price_editor = Label(archived_edit_frame, text="*Sold Price:")

archived_purchased_from_editor = Entry(archived_edit_frame, justify="center")
archived_item_name_editor = Entry(archived_edit_frame, justify="center")
archived_item_price_editor = Entry(archived_edit_frame, justify="center")
archived_item_size_editor = Entry(archived_edit_frame, justify="center")
archived_item_color_editor = Entry(archived_edit_frame, justify = "center")
archived_item_quantity_editor = Entry(archived_edit_frame, justify="center")
archived_item_quantity_editor.insert(END, "1")
archived_item_quantity_editor.config(state = DISABLED)
archived_item_purchase_date_editor = Entry(archived_edit_frame, justify="center")
archived_item_sold_date_editor = Entry(archived_edit_frame, justify = "center")
archived_item_sold_price_editor = Entry(archived_edit_frame, justify="center")

archived_location_editor.grid(row=0, column=0, padx=5, pady=5)
archived_purchased_from_editor.grid(row=0, column=1, padx=5, pady=5)
archived_name_editor.grid(row=1, column=0, padx=5, pady=5)
archived_item_name_editor.grid(row=1, column=1, padx=5, pady=5)
archived_price_editor.grid(row=2, column=0, padx=5, pady=5)
archived_item_price_editor.grid(row=2, column=1, padx=5, pady=5)
archived_size_editor.grid(row=3, column=0, padx=5, pady=5)
archived_item_size_editor.grid(row=3, column=1, padx=5, pady=5)
archived_color_editor.grid(row=4, column=0, padx=5, pady=5)
archived_item_color_editor.grid(row=4, column=1, padx=5, pady=5)
archived_quantity_editor.grid(row=5, column=0, padx=5, pady=5)
archived_item_quantity_editor.grid(row=5, column=1, padx=5, pady=5)
archived_purchase_date_editor.grid(row=6, column=0, padx=5, pady=5)
archived_item_purchase_date_editor.grid(row=6, column=1, padx=5, pady=5)
archived_sold_date_editor.grid(row=7, column=0, padx=5, pady=5)
archived_item_sold_date_editor.grid(row=7, column=1, padx=5, pady=5)
archived_sold_price_editor.grid(row=8, column=0, padx=5, pady=5)
archived_item_sold_price_editor.grid(row=8, column=1, padx=5, pady=5)

current_location_editor = Label(current_edit_frame, text="*Where item was purchased from:")
current_name_editor = Label(current_edit_frame, text="*Item:")
current_price_editor = Label(current_edit_frame, text="*Price:")
current_size_editor = Label(current_edit_frame, text="Size:")
current_color_editor = Label(current_edit_frame, text = "Color/Style:")
current_quantity_editor = Label(current_edit_frame, text="Quantity:")
current_purchase_date_editor = Label(current_edit_frame, text="*Purchase Date (mm/dd/yyyy):")
current_sold_date_editor = Label(current_edit_frame, text = "Sold Date (mm/dd/yyyy):")
current_sold_price_editor = Label(current_edit_frame, text="Sold Price:")

current_purchased_from_editor = Entry(current_edit_frame, justify="center")
current_item_name_editor = Entry(current_edit_frame, justify="center")
current_item_price_editor = Entry(current_edit_frame, justify="center")
current_item_size_editor = Entry(current_edit_frame, justify="center")
current_item_color_editor = Entry(current_edit_frame, justify = "center")
current_item_quantity_editor = Entry(current_edit_frame, justify="center")
current_item_quantity_editor.insert(END, "1")
current_item_quantity_editor.config(state = DISABLED)
current_item_purchase_date_editor = Entry(current_edit_frame, justify="center")
current_item_sold_date_editor = Entry(current_edit_frame, justify = "center")
current_item_sold_price_editor = Entry(current_edit_frame, justify="center")

current_location_editor.grid(row=0, column=0, padx=5, pady=5)
current_purchased_from_editor.grid(row=0, column=1, padx=5, pady=5)
current_name_editor.grid(row=1, column=0, padx=5, pady=5)
current_item_name_editor.grid(row=1, column=1, padx=5, pady=5)
current_price_editor.grid(row=2, column=0, padx=5, pady=5)
current_item_price_editor.grid(row=2, column=1, padx=5, pady=5)
current_size_editor.grid(row=3, column=0, padx=5, pady=5)
current_item_size_editor.grid(row=3, column=1, padx=5, pady=5)
current_color_editor.grid(row=4, column=0, padx=5, pady=5)
current_item_color_editor.grid(row=4, column=1, padx=5, pady=5)
current_quantity_editor.grid(row=5, column=0, padx=5, pady=5)
current_item_quantity_editor.grid(row=5, column=1, padx=5, pady=5)
current_purchase_date_editor.grid(row=6, column=0, padx=5, pady=5)
current_item_purchase_date_editor.grid(row=6, column=1, padx=5, pady=5)
current_sold_date_editor.grid(row=7, column=0, padx=5, pady=5)
current_item_sold_date_editor.grid(row=7, column=1, padx=5, pady=5)
current_sold_price_editor.grid(row=8, column=0, padx=5, pady=5)
current_item_sold_price_editor.grid(row=8, column=1, padx=5, pady=5)

# Entry boxes for UPS frame
ups_tracking_number_entry = Entry(ups_tracking_add_new_item, justify="center")
ups_tracking_number_entry.grid(row = 0, column = 1, pady = 10, padx = 10)
ups_shipper_entry = Entry(ups_tracking_add_new_item, justify = "center")
ups_shipper_entry.grid(row = 1, column = 1, padx = 10, pady = 10 )

# Entry boxes for USPS frame
usps_tracking_number_entry = Entry(usps_tracking_add_new_item, justify="center")
usps_tracking_number_entry.grid(row = 0, column = 1, pady = 10, padx = 10)
usps_shipper_entry = Entry(usps_tracking_add_new_item, justify = "center")
usps_shipper_entry.grid(row = 1, column = 1, padx = 10, pady = 10 )

# Labels for current entry boxes
current_location = Label(current_add_new_item, text="*Where item was purchased from:")
current_name = Label(current_add_new_item, text="*Item:")
current_price = Label(current_add_new_item, text="*Price:")
current_size = Label(current_add_new_item, text="Size:")
current_color = Label(current_add_new_item, text = "Color/Style:")
current_quantity = Label(current_add_new_item, text="Quantity:")
current_purchase_date = Label(current_add_new_item, text="*Purchase Date (mm/dd/yyyy):")
current_sold_date = Label(current_add_new_item, text = "Sold Date (mm/dd/yyyy):")
current_sold_price = Label(current_add_new_item, text="Sold Price (leave 0 if not sold):")
current_requirement = Label(current_add_new_item, text="*Required fields", fg="red", font="TkDefaultFont 9 italic")

# Labels for archived entry boxes
archived_location = Label(archived_add_new_item, text="*Where item was purchased from:")
archived_name = Label(archived_add_new_item, text="*Item:")
archived_price = Label(archived_add_new_item, text="*Price:")
archived_size = Label(archived_add_new_item, text="Size:")
archived_color = Label(archived_add_new_item, text = "Color/Style:")
archived_quantity = Label(archived_add_new_item, text="Quantity:")
archived_purchase_date = Label(archived_add_new_item, text="*Purchase Date (mm/dd/yyyy):")
archived_sold_date = Label(archived_add_new_item, text = "*Sold Date (mm/dd/yyyy):")
archived_sold_price = Label(archived_add_new_item, text="*Sold Price:")
archived_requirement = Label(archived_add_new_item, text="*Required fields", fg="red", font="TkDefaultFont 9 italic")

# Label for UPS frame
ups_tracking_number_label = Label(ups_tracking_add_new_item, text="Enter tracking number:").grid(row = 0, column = 0,padx = 10)
ups_shipper_label = Label(ups_tracking_add_new_item, text = "Purchased from:").grid(row = 1, column = 0, padx = 10)

usps_tracking_number_label = Label(usps_tracking_add_new_item, text="Enter tracking number:").grid(row = 0, column = 0,padx = 10)
usps_shipper_label = Label(usps_tracking_add_new_item, text = "Purchased from:").grid(row = 1, column = 0, padx = 10)


ups_tracking_editor = Label(edit_ups_frame, text="Tracking Number:")
ups_shipper_label_editor = Label(edit_ups_frame, text = "Purchased from:")

ups_tracking_entry = Entry(edit_ups_frame, justify = "center")
ups_shipper_entry_editor = Entry(edit_ups_frame, justify = "center")

ups_tracking_editor.grid(row=0, column=0, padx=10, pady=10)
ups_tracking_entry.grid(row=0, column=1, padx=10, pady=10)
ups_shipper_label_editor.grid(row=1, column=0, padx=10, pady=10)
ups_shipper_entry_editor.grid(row=1, column=1, padx=10, pady=10)
ups_save_button = Button(edit_ups_frame, text="Save Changes", command=update_ups)
ups_save_button.grid(row=7, column=1, pady= 10)

usps_tracking_editor = Label(edit_usps_frame, text="Tracking Number:")
usps_shipper_label_editor = Label(edit_usps_frame, text = "Purchased from:")

usps_tracking_entry = Entry(edit_usps_frame, justify = "center")
usps_shipper_entry_editor = Entry(edit_usps_frame, justify = "center")

usps_tracking_editor.grid(row=0, column=0, padx=10, pady=10)
usps_tracking_entry.grid(row=0, column=1, padx=10, pady=10)
usps_shipper_label_editor.grid(row=1, column=0, padx=10, pady=10)
usps_shipper_entry_editor.grid(row=1, column=1, padx=10, pady=10)
usps_save_button = Button(edit_usps_frame, text="Save Changes", command=update_usps)
usps_save_button.grid(row=7, column=1, pady= 10)

# Displays current entry boxes and labels
current_location.grid(row=0, column=0, padx=5, pady=5)
current_purchased_from.grid(row=0, column=1, padx=10, pady=5)
current_name.grid(row=1, column=0, padx=5, pady=5)
current_item_name.grid(row=1, column=1, padx=10, pady=5)
current_price.grid(row=2, column=0, padx=5, pady=5)
current_item_price.grid(row=2, column=1, padx=10, pady=5)
current_size.grid(row=3, column=0, padx=5, pady=5)
current_item_size.grid(row=3, column=1, padx=10, pady=5)
current_color.grid(row=4, column=0, padx=5, pady=5)
current_item_color.grid(row=4, column=1, padx=5, pady=5)
current_quantity.grid(row=5, column=0, padx=5, pady=5)
current_item_quantity.grid(row=5, column=1, padx=10, pady=5)
current_purchase_date.grid(row=6, column=0, padx=5, pady=5)
current_item_purchase_date.grid(row=6, column=1, padx=10, pady=5)
current_sold_date.grid(row=7, column=0, padx=5, pady=5)
current_item_sold_date.grid(row=7, column=1, padx=5, pady=5)
current_sold_price.grid(row=8, column=0, padx=5, pady=5)
current_item_sold_price.grid(row=8, column=1, padx=10, pady=5)
current_requirement.grid(row=9, column=0, padx=5, pady=5)
current_submit.grid(row=9, column=1, padx=10, pady=5)

# Displays archived entry boxes and labels
archived_location.grid(row=0, column=0, padx=5, pady=5)
archived_purchased_from.grid(row=0, column=1, padx=10, pady=5)
archived_name.grid(row=1, column=0, padx=5, pady=5)
archived_item_name.grid(row=1, column=1, padx=10, pady=5)
archived_price.grid(row=2, column=0, padx=5, pady=5)
archived_item_price.grid(row=2, column=1, padx=10, pady=5)
archived_size.grid(row=3, column=0, padx=5, pady=5)
archived_item_size.grid(row=3, column=1, padx=10, pady=5)
archived_color.grid(row=4, column=0, padx=5, pady=5)
archived_item_color.grid(row=4, column=1, padx=5, pady=5)
archived_quantity.grid(row=5, column=0, padx=5, pady=5)
archived_item_quantity.grid(row=5, column=1, padx=10, pady=5)
archived_purchase_date.grid(row=6, column=0, padx=5, pady=5)
archived_item_purchase_date.grid(row=6, column=1, padx=10, pady=5)
archived_sold_date.grid(row=7, column=0, padx=5, pady=5)
archived_item_sold_date.grid(row=7, column=1, padx=5, pady=5)
archived_sold_price.grid(row=8, column=0, padx=5, pady=5)
archived_item_sold_price.grid(row=8, column=1, padx=10, pady=5)
archived_requirement.grid(row=9, column=0, padx=5, pady=5)
archived_submit.grid(row=9, column=1, padx=10, pady=5)

# Makes current table
current_columns = ("ID","Purchased From","Item","Price","Size","Color/Style","Quantity","Purchase Date","Sold Date","Sold Price","Profit")
current_record_table = ttk.Treeview(current_inventory, columns=current_columns, show="headings")

current_record_table.column("ID", anchor=CENTER, width=50, stretch=0)
current_record_table.column("Purchased From", anchor=CENTER)
current_record_table.column("Item", anchor=CENTER)
current_record_table.column("Price", anchor=CENTER)
current_record_table.column("Size", anchor=CENTER, width = 120, stretch=0)
current_record_table.column("Color/Style", anchor=CENTER)
current_record_table.column("Quantity", anchor=CENTER, width = 70, stretch = 0)
current_record_table.column("Purchase Date", anchor=CENTER)
current_record_table.column("Sold Date", anchor=CENTER)
current_record_table.column("Sold Price", anchor=CENTER, width = 120, stretch = 0)
current_record_table.column("Profit", anchor=CENTER, width = 120, stretch = 0)

for col in current_columns:
    current_record_table.heading(col, text=col, command=lambda _col=col: \
                     current_treeview_sort_column(current_record_table, _col, False))

style = ttk.Style()
style.configure("Treeview.Heading", foreground="green", font="TkDefaultFont 9 bold")

current_record_table.place(x = 125, y= 100, height = 850)

current_scrollbar = Scrollbar(current_inventory, orient = "vertical", command = current_record_table.yview)
current_scrollbar.place(x=1800, y= 100, height = 850)
current_record_table.configure(yscrollcommand = current_scrollbar.set)


# Makes archived table
archived_columns = ("ID","Purchased From","Item","Price","Size","Color/Style","Quantity","Purchase Date","Sold Date","Sold Price","Profit")
archived_record_table = ttk.Treeview(archived_inventory, columns=archived_columns, show="headings")

archived_record_table.column("ID", anchor=CENTER, width=50, stretch=0)
archived_record_table.column("Purchased From", anchor=CENTER)
archived_record_table.column("Item", anchor=CENTER)
archived_record_table.column("Price", anchor=CENTER)
archived_record_table.column("Size", anchor=CENTER, width = 120, stretch=0)
archived_record_table.column("Color/Style", anchor=CENTER)
archived_record_table.column("Quantity", anchor=CENTER, width = 70, stretch = 0)
archived_record_table.column("Purchase Date", anchor=CENTER)
archived_record_table.column("Sold Date", anchor=CENTER)
archived_record_table.column("Sold Price", anchor=CENTER, width = 120, stretch = 0)
archived_record_table.column("Profit", anchor=CENTER, width = 120, stretch = 0)

for col in archived_columns:
    archived_record_table.heading(col, text=col, command=lambda _col=col: \
                     archived_treeview_sort_column(archived_record_table, _col, False))

style = ttk.Style()
style.configure("Treeview.Heading", foreground="green", font="TkDefaultFont 9 bold")

archived_record_table.place(x = 125, y= 100, height = 850)

archived_scrollbar = Scrollbar(archived_inventory, orient = "vertical", command = archived_record_table.yview)
archived_scrollbar.place(x=1800, y= 100, height = 850)
archived_record_table.configure(yscrollcommand = archived_scrollbar.set)


# Makes UPS record table
ups_columns = ("ID", "Tracking Number", "Purchased From", "Status", "Current Location", "Last Updated by UPS", "Estimated Delivery Date")
ups_record_table = ttk.Treeview(ups_main, columns=ups_columns, show="headings")

ups_record_table.column("ID", anchor=CENTER, width=50, stretch=0)
ups_record_table.column("Tracking Number", anchor=CENTER, width = 200)
ups_record_table.column("Purchased From", anchor=CENTER, width = 200)
ups_record_table.column("Status", anchor=CENTER, width = 300)
ups_record_table.column("Current Location", anchor=CENTER, width = 200)
ups_record_table.column("Last Updated by UPS", anchor=CENTER, width = 300)
ups_record_table.column("Estimated Delivery Date", anchor = CENTER, width = 200)

for col in ups_columns:
    ups_record_table.heading(col, text=col, command=lambda _col=col: \
                     ups_treeview_sort_column(ups_record_table, _col, False))

style = ttk.Style()
style.configure("Treeview.Heading", foreground="green", font="TkDefaultFont 9 bold")

ups_record_table.place(x=225, y=100, height = 850)

ups_scrollbar = Scrollbar(ups_main, orient = "vertical", command = ups_record_table.yview)
ups_scrollbar.place(x=1675, y= 100, height = 850)
ups_record_table.configure(yscrollcommand = ups_scrollbar.set)


# Makes USPS record table
usps_columns = ("ID", "Tracking Number", "Purchased From", "Status", "Current Location", "Last Updated by USPS", "Estimated Delivery Date")
usps_record_table = ttk.Treeview(usps_main, columns=usps_columns, show="headings")

usps_record_table.column("ID", anchor=CENTER, width=50, stretch=0)
usps_record_table.column("Tracking Number", anchor=CENTER, width = 200)
usps_record_table.column("Purchased From", anchor=CENTER, width = 200)
usps_record_table.column("Status", anchor=CENTER, width = 300)
usps_record_table.column("Current Location", anchor=CENTER, width = 200)
usps_record_table.column("Last Updated by USPS", anchor=CENTER, width = 300)
usps_record_table.column("Estimated Delivery Date", anchor = CENTER, width = 200)

for col in usps_columns:
    usps_record_table.heading(col, text=col, command=lambda _col=col: \
                     usps_treeview_sort_column(ups_record_table, _col, False))

style = ttk.Style()
style.configure("Treeview.Heading", foreground="green", font="TkDefaultFont 9 bold")

usps_record_table.place(x=225, y=100, height = 850)

usps_scrollbar = Scrollbar(usps_main, orient = "vertical", command = usps_record_table.yview)
usps_scrollbar.place(x=1675, y= 100, height = 850)
usps_record_table.configure(yscrollcommand = usps_scrollbar.set)

total_label = Label(stats, textvariable = total_label_startup, font ="TkDefaultFont 12 bold", foreground = "red")
total_label.grid(pady= 10, padx =5)

overall_profit_label = Label(stats, textvariable = overall_profit_startup, font ="TkdefaultFont 12 bold", foreground = "green")
overall_profit_label.grid(pady = 10, padx =5)

current_item_count_label = Label(current_inventory, textvariable= current_item_count, font="TkDefaultFont 10 bold").place(x=640, y=65)
archived_item_count_label = Label(archived_inventory, textvariable= archived_item_count, font="TkDefaultFont 10 bold").place(x=640, y=65)

current_record_table.bind("<ButtonRelease-1>", select_item_current)
archived_record_table.bind("<ButtonRelease-1>", select_item_archived)
ups_record_table.bind("<ButtonRelease-1>", select_item_ups)
usps_record_table.bind("<ButtonRelease-1>", select_item_usps)


raise_frame(main_screen)
display_stats()
# startup()
# graph_current_expense()
master.mainloop()
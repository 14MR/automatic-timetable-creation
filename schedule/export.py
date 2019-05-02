import xlsxwriter

from users.models import Group, YearGroup
from .models import Event, Timeslot
from .enums import DaysOfWeek

days_in_week = 7


def stringify_class(Class):
    pass


# Receives filename, year and type of the semester
def s(filename="default", year=2019, type=0):
    week_color = "#3c78d8"
    color_bank = []
    workbook = xlsxwriter.Workbook(filename + ".xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.set_row(0, 30)
    worksheet.set_column(0, 0, 12)
    groups_format = workbook.add_format(
        {"bold": True, "font_size": 12, "align": "center", "valign": "vcenter"}
    )
    time_format = workbook.add_format(
        {"font_size": 12, "align": "center", "valign": "vcenter"}
    )
    month_format = workbook.add_format(
        {"bold": True, "font_size": 12, "align": "center", "valign": "vcenter"}
    )
    month_format.set_bg_color(week_color)
    event_format = workbook.add_format(
        {"font_size": 12, "align": "center", "valign": "vcenter"}
    )

    events = Event.objects.all()
    bold = workbook.add_format({"font_size": 12, "bold": True})
    italic = workbook.add_format({"font_size": 12, "italic": True})

    groups = (
        Group.objects.filter(
            events__schedule__semester__year=year, events__schedule__semester__type=type
        )
        .distinct()
        .order_by("-study_year__year", "number")
    )
    # Write timeslots
    cur_row = 1
    for i in range(days_in_week):
        worksheet.set_row(cur_row, 15)
        worksheet.write(cur_row, 0, DaysOfWeek.get_choice(i).label, month_format)
        timeslots = Timeslot.objects.order_by("starting_time").filter(day_of_week=i)
        cur_row += 1
        for j in range(timeslots.count()):
            worksheet.set_row(cur_row, 70)
            worksheet.write(
                cur_row,
                0,
                f"{timeslots[j].starting_time.strftime('%H:%M')}-\
{timeslots[j].ending_time.strftime('%H:%M')}",
                time_format,
            )
            cur_row += 1

    # Write groups
    for i in range(1, len(groups) + 1):
        worksheet.set_column(i, i, 30)
        worksheet.write(0, i, str(groups[i - 1]), groups_format)

    # Write events
    cur_column = 1
    was_merged = set()
    for i in range(len(groups)):
        cur_row = 2
        for j in range(days_in_week):
            timeslots = Timeslot.objects.order_by("starting_time").filter(day_of_week=j)
            cur_ev = 0
            evs = events.filter(timeslot__day_of_week=j, group__id=groups[i].id)
            for k in range(len(timeslots)):
                if cur_ev >= len(evs):
                    break
                if evs[cur_ev].timeslot.starting_time == timeslots[k].starting_time:
                    cur_event = evs[cur_ev]
                    if cur_event not in was_merged and len(cur_event.group.all()) > 1:
                        was_merged.add(cur_event)
                        worksheet.merge_range(
                            cur_row,
                            cur_column,
                            cur_row,
                            cur_column + len(cur_event.group.all()) - 1,
                            "",
                            event_format,
                        )
                    worksheet.write_rich_string(
                        cur_row,
                        cur_column,
                        f"{cur_event.current_class.course.title}\n",
                        bold,
                        f"{cur_event.current_class.teacher.first_name} {cur_event.current_class.teacher.last_name}\n",
                        italic,
                        f"{cur_event.room.number}\n",
                        event_format,
                    )

                    cur_ev += 1
                cur_row += 1
        cur_column += 1
    print(worksheet.print_area(0, 0, 3, 3))
    cur_column = 1
    cur_row = 1
    # instead of 2 - number of year_groups
    for k in range(2):
        for i in range(days_in_week):
            timeslots = Timeslot.objects.order_by("starting_time").filter(day_of_week=i)
            cur_row += 1
            for j in range(timeslots.count()):
                cur_row += 1

    workbook.close()


# if __name__ == '__main__':
# export_to_xls()
# export_to_xls()

"""
from schedule.export import *
"""

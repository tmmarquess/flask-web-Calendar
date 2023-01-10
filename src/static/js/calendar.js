const calendar = document.querySelector(".calendar"),
    date = document.querySelector(".date"),
    daysContainer = document.querySelector(".days"),
    prev = document.querySelector(".prev"),
    next = document.querySelector(".next")

let today = new Date()
let activeDay;
let month = today.getMonth()
let year = today.getFullYear()

const months = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro"
]

const eventsArray = [
    {
        day: 8,
        month: 1,
        year: 2023
    },
    {
        day: 10,
        month: 1,
        year: 2023
    },
    {
        day: 11,
        month: 1,
        year: 2023
    },
    {
        day: 15,
        month: 1,
        year: 2023
    },
    {
        day: 18,
        month: 1,
        year: 2023
    },
    {
        day: 22,
        month: 1,
        year: 2023
    },
    {
        day: 26,
        month: 1,
        year: 2023
    },
    {
        day: 31,
        month: 1,
        year: 2023
    }
]

function initCalendar() {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const prevLastDay = new Date(year, month, 0)
    const prevDays = prevLastDay.getDate()
    const lastDate = lastDay.getDate()
    const day = firstDay.getDay()
    const firstWeekDay = firstDay.getDay()
    let nextDays

    // Logic to view each month with 6 weeks

    console.log(lastDate)

    if (lastDate == 31) {
        if (firstWeekDay == 5 || firstWeekDay == 6) {
            nextDays = 7 - lastDay.getDay() - 1
        } else {
            nextDays = 14 - lastDay.getDay() - 1
        }
    } else if (lastDate == 30) {
        if (firstWeekDay == 6) {
            nextDays = 7 - lastDay.getDay() - 1
        } else {
            nextDays = 14 - lastDay.getDay() - 1
        }
    } else if (lastDate == 28) {
        const lastWeekDay = lastDay.getDay()
        if (lastWeekDay == 6) {
            nextDays = 21 - lastDay.getDay() - 1
        } else {
            nextDays = 14 - lastDay.getDay() - 1
        }
    } else {
        nextDays = 14 - lastDay.getDay() - 1
    }

    // Update the date at the top of the calendar
    date.innerHTML = months[month] + " " + year

    let days = ""

    // Previous month days
    for (let p = day; p > 0; p--) {
        days += `<div class="day prev-date">${prevDays - p + 1}</div>`
    }

    // Current month days
    for (let c = 1; c <= lastDate; c++) {
        let hasEvent = false

        eventsArray.forEach((eventObj) => {
            if (
                eventObj.day == c &&
                eventObj.month == month + 1 &&
                eventObj.year == year
            ) {
                hasEvent = true
            }
        })

        if (
            c === new Date().getDate() &&
            year == new Date().getFullYear() &&
            month === new Date().getMonth()
        ) {
            if (hasEvent) {
                days += `<div class="day today event">${c}</div>`
            } else {
                days += `<div class="day today">${c}</div>`
            }
        } else {
            if (hasEvent) {
                days += `<div class="day event">${c}</div>`
            } else {
                days += `<div class="day">${c}</div>`
            }
        }
    }

    // Next month days
    for (let n = 1; n <= nextDays; n++) {
        days += `<div class="day next-date">${n}</div>`
    }

    daysContainer.innerHTML = days
}

initCalendar()

function prevMonth() {
    month--;
    if (month < 0) {
        month = 11;
        year--;
    }
    initCalendar()
}

function nextMonth() {
    month++;
    if (month > 11) {
        month = 0
        year++
    }
    initCalendar()
}

prev.addEventListener("click", prevMonth)
next.addEventListener("click", nextMonth)
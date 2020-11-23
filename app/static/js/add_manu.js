function checkbox_pressed(element) {
    document.getElementById(element.id.slice(0, -3) + "_btn").disabled = !element.checked;
    document.getElementById(element.id.slice(0, -3)).setAttribute("value", "")
}

function update_master(element) {
    const barcode = document.getElementById("barcode");
    update_parts(element, barcode);
}

function update_comp_master(element) {
    const barcode = document.getElementById("comp_barcode");
    update_parts(element, barcode);
}

function update_parts(element, barcode) {
    const id = element.id;
    const myRegexp = /\.([^.]+)\./g;
    const match = myRegexp.exec(barcode.value);
    if (match != null) {
        document.getElementById(id.slice(0, -4)).setAttribute("value", match[1]);
        document.getElementById(id.slice(0, -7) + "start").setAttribute("value", barcode.value.indexOf("."));
        barcode.value = barcode.value.split('.').join("");
    }
}

function update_date(element) {
    const barcode = document.getElementById("barcode");
    const myRegexp = /\.([^.]+)\./g;
    const match = myRegexp.exec(barcode.value);

    if (match != null) {
        const date = match[1].replace(/\//g, "-");
        const month = parseInt(date.slice(5, 7), 10);
        const large_month = [1, 3, 5, 7, 8, 10, 12];
        if (large_month.includes(month)) {
            document.getElementById($(element).attr("id").slice(0, -4)).setAttribute("value", date + "-31");
        } else if (month === 2) {
            document.getElementById($(element).attr("id").slice(0, -4)).setAttribute("value", date + "-28");
        } else {
            document.getElementById($(element).attr("id").slice(0, -4)).setAttribute("value", date + "-30");
        }
        document.getElementById($(element).attr("id").slice(0, -3) + "start").setAttribute("value", barcode.value.indexOf("."));
        barcode.value = barcode.value.split('.').join("");
    }
}
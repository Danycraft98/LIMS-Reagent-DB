let counter = 1;
let properties = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

function update_all(element) {
    properties = element.value.split(",");
    update_barcode();
}

function update_barcode() {
    const barcode = document.getElementById("barcode").value;
    if (properties[1] >= 0) {
        document.getElementById("part_num").setAttribute("value", barcode.slice(properties[1], properties[2]));
    } else {
        document.getElementById("part_num").setAttribute("value", "");
    }

    if (properties[3] >= 0) {
        document.getElementById("lot_num").setAttribute("value", barcode.slice(properties[3], properties[4]));
    } else {
        document.getElementById("lot_num").setAttribute("value", "");
    }

    if (properties[5] >= 0) {
        document.getElementById("exp_date").setAttribute("value", get_date(barcode.slice(properties[5], properties[6])));
    } else {
        document.getElementById("exp_date").setAttribute("value", "");
    }
}
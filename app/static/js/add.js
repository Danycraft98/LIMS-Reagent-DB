function collapse(element) {
    const arrow = element.firstChild;
    if (element.innerText.includes('Expand')) {
        arrow.className = arrow.className.replace('down', 'up');
        element.innerHTML = element.innerHTML.replace('Expand', 'Collapse');
    } else {
        arrow.className = arrow.className.replace('up', 'down');
        element.innerHTML = element.innerHTML.replace('Collapse', 'Expand');
    }
}

function get_date(year_month) {
    const month30 = [4,6,9,11];
    const month31 = [1,3,5,7,8,10,12];
    let result = year_month.replace('/','-');
    const month = parseInt(year_month.slice(-2));
    if (month30.includes(month)) {
        result += '-30'
    } else if (month31.includes(month)) {
        result += '-31'
    } else if (month === 2) {
        result += '-28'
    }
    return result;
}

function clone_element(element) {
    let kit_num = '';
    if (element.id.split('_')[0].includes('k')) {
        kit_num = element.id.split('_')[0] + '_';
    }
    let counter = parseInt(document.getElementById(kit_num + 'comps').lastElementChild.id.split('p')[1]) + 1;

    let div_num = element.id.match(/\d+$/);
    const div = document.getElementById(kit_num + 'comp' + div_num);
    console.log(div_num)
    for (let k = 0; k < document.getElementById(kit_num + 'copy_num' + div_num).value; k++) {
        const clone = div.cloneNode(true);
        clone.id = clone.id.replace(/\d+$/, '') + counter.toString();
        clone.childNodes.forEach(function (element) {
            if (element.tagName === 'DIV') {
                element.childNodes.forEach(function (sub_element) {
                    if (sub_element.childNodes.length > 3) {
                        let input = sub_element.children;
                        if (input[0].tagName !== 'LABEL') {
                            input[0].id = input[0].id.replace(/\d+$/, '') + counter.toString();
                        }
                        if (input[1].tagName !== 'LABEL') {
                            input[1].id = input[1].id.replace(/\d+$/, '') + counter.toString();
                        }
                        if (input[3] !== undefined) {
                            input[3].id = input[3].id.replace(/\d+$/, '') + counter.toString();
                        }
                    }
                });
            }
        });

        clone.removeAttribute('hidden');
        document.getElementById(kit_num + 'comps').appendChild(clone);
        counter++;
    }
}

function remove_element(element) {
    const containerDiv = element.parentElement.parentElement.parentElement.id;
    document.getElementById(containerDiv).remove();
}

function confirmMsg() {
    return confirm('Are you sure?');
}

function deleteMsg(deletable) {
    if (deletable === 'True') {
        return confirmMsg();
    } else {
        alert('This cannot be deleted.');
        return false;
    }
}

function editMsg(deletable) {
    if (deletable === 'True') {
        return true;
    } else {
        alert('This cannot be edited.');
        document.getElementById('edit_btn').setAttribute('data-target','#None')
        return false;
    }
}

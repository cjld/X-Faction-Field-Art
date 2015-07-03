function saveFile(T,content) {//保存
    var filename=document.all(T).value;
    var win=window.open('','','top=10000,left=10000');
    win.document.write(document.all(content).innerText);
    win.document.execCommand('SaveAs','',filename)
    win.close();
}

var data = []

for (var k in window.portals) {
    p = window.portals[k];
    if (p._map) {
        data.push(
            {
                "LatLng" : p.getLatLng(),
                "name" : p.options.data.title,
            });
    }
}

var ss = JSON.stringify(data)

//saveFile("portals.json", ss);
window.clipboardData.setData("Text", ss);

function getRandomInt(min, max) {
	    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function contains(arr, e){
    for (var i = 0; i < arr.length; ++i){
        if (e[0] == arr[i][0] && e[1] == arr[i][1]) return true;
    }
    return false;
}

var mines = [];
var remain = n * n - mines_count;
var generated = false;
var state = "game"
var table = document.getElementById("map");

function generate(_x, _y){
    if (mines_count >= (n*n)){
        alert("too many mines");
        mines_count = 1;
        remain = n * n - mines_count;
    }
    
    var arr = [] 
    for (var i = 0; i < n * n; ++i){
        arr[i] = [Math.floor(i / n), i % n];
    }
    for (var i = 0; i < n * n * n; ++i){
        var a = getRandomInt(0, n * n - 1);
        var b = getRandomInt(0, n * n - 1);
        
        var tmp = arr[a];
        arr[a] = arr[b];
        arr[b] = tmp;
    }
    var kostyl = 0;
    for (var i = 0; i < mines_count; ++i){
        if (arr[i][0] == _x && arr[i][1] == _y)
            kostyl += 1;
        mines[i] = arr[i + kostyl];
    }
}

function open(x, y){
    var e = table.children[x].children[y];
    
    const dx = [-1, -1, -1, 0, 0, 1, 1, 1];
    const dy = [-1, 0, 1, -1, 1, -1, 0, 1];

    var value = 0;

    for (var i = 0; i < 8; ++i){
        var _x = x + dx[i];
        var _y = y + dy[i];
        
        if (_x < 0 || _y < 0 || _x >= n || _y >= n){
            continue;
        }
        
        if (contains(mines, [_x, _y])){
            value += 1;
        }
    }
    e.setAttribute("class", "opened");
    if (value == 0){
        for (var i = 0; i < 8; ++i){
            var _x = x + dx[i];
            var _y = y + dy[i];
        
            if (_x < 0 || _y < 0 || _x >= n || _y >= n){
                continue;
            }
            
            var t = table.children[_x].children[_y];
            
            if (t.classList.contains("opened") || contains(mines, [_x, _y])){
                continue;
            }
            
            open(_x, _y);
        }
    }
     
    if (value > 0) 
        e.append(value);
    remain -= 1;
    if (remain <= 0){
        alert("GG EZ");
        state = "win";
    }
        
}

function tap(e) {
    if (state != "game")
        return;
    
    var x = +this.getAttribute("data-x");
    var y = +this.getAttribute("data-y");
    
    if (!generated){
        generate(x, y);
        generated = true;
    }
    
    if (this.classList.contains("unknown")){
        var coords = [x, y]
        if (contains(mines, coords)){
            for (var i = 0; i < mines_count; ++i){
                x = mines[i][0];
                y = mines[i][1];

                var t = table.children[x].children[y];
                t.setAttribute("class", "BOOM");
            }
            alert("T_T");
            state = "lose";
        }
        else{
            open(x, y);
        }
    }
}

function mark(e) {
    e.preventDefault(); 
    if (state != "game" || !generated)
        return false;

    if (this.classList.contains("unknown")) {
        list = this.classList;
        if (list.contains("marked")) {
            this.classList.remove('marked')
        }
        else {
            this.classList.add('marked')
        }
    }

    return false;
}

for (var i = 0; i < n; ++i){
    var row = document.createElement("tr");
    
    for (var j = 0; j < n; ++j){
        var cell = document.createElement("td");
        cell.onclick = tap;
        cell.addEventListener('contextmenu', mark, false);
        
        cell.setAttribute("data-x", i);
        cell.setAttribute("data-y", j);
        cell.setAttribute("class", "unknown");
    
        row.appendChild(cell);
    }
    
    table.appendChild(row);
}











function printx(x){
	if(x != 0){
		printx(x/10);
		var b;
		b = x%10 + 48;
		send b;
	}
}

function print(y){
	if(y == 0){
		send 40;
	}else{
		printx(y);
	}
	send 10;
}

function scan(){
	var i;
	var j;
	i = recv; j = 0;
	while (i != 10) {
		j = j * 10 + (i - 48);
		i = recv;
	}
	return j;
}
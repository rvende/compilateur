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
		send 48;
	}else{
		if(y < 0){
			send 45;
			printx(-y);
		}else{
			printx(y);
		}
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

function puissance(a,b){
	var c;
	c = 1;
	var i;
	for(i=0;i<10;i = i+1){
		c = c*a;
	}
	return c;
}function main() { continue; print(32); return 0;}
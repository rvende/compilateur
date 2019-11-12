function somme(n,m,k){ 
	if(n<=0){ 
		return 2+m+k;  
	}else{ 
		if(n == 15){ 
			return n;
		}
			
			var i; 
			for(i =0;i<3;i=i+1){ 
				n = n-1; 
				if(n == 12){ 
					break;
			 	}
			} 
		return n*m+k + somme(n-1,m,k-1) + k -2; 
		
	} 
} 
function main() { 
	var a; 
	a = 2; 
	a = a+ somme(22,4,2); 
	print(a);
	return a;
}


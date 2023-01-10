<script th:inline="javascript">



	var ingre = [[${json}]];
	var ewg = [[${ewg}]];
	var ewglist = ewg.split(",");
	var age = [[${cos.productAgeLikes}]];
	var agelist = age.split("|");
	console.log(agelist != 'None');
	var sex = [[${cos.productSexLikes}]];
	var sexlist = sex.split("|");
	console.log(sexlist)

	$(function(){
  	  		var chartArea = document.getElementById('myChart').getContext('2d');
	// 차트를 생성한다. 
	var myChart = new Chart(chartArea, {
		plugins:[ChartDataLabels],
	data :  chartData,
	options : chartOptions
  	  			
  	  		})
  	  	})

	var chartData = {
		labels : ['지성','건성','민감성'],
	datasets : [
	{
		type : 'bar',
	label : 'good',

	data : [ingre[1],ingre[5],ingre[9]],
	datalabels:{
		// 너무 흐리다 싶어서 잘 보이도록 완전히 검게..
		color:'white',                      // 배경색을 어떻게 세팅했냐에 따라 적절히..
	// pixel 단위이고, 수치로 입력
	align: 'right',
	anchor: 'center'
  			


  				    },
	backgroundColor : 'rbga(255,99,132,0.2)',
	borderColor : 'rgba(255, 99, 132, 1)',
	borderWidth : 1
  				},
	{
		type : 'bar',
	label : 'bad',
	data : [ingre[3],ingre[7],ingre[11]],
	datalabels:{
		color:'white',
	align: 'right',
	anchor: 'center'
		


			    },
	backgroundColor : 'rbga(100,99,132,0.2)',
	borderColor : 'rgba(100, 99, 132, 1)',
	borderWidth : 1
  				},


	]
  		
  		};

	var chartOptions = {
		indexAxis: 'y',
  			

  		};

	$(function(){
  	  		var chartArea2 = document.getElementById('myChart2').getContext('2d');
	// 차트를 생성한다. 
	var myChart2 = new Chart(chartArea2, {
		plugins:[ChartDataLabels],
	type : 'bar',
	data :  chartData2,
	options : chartOptions2
  	  			
  	  		})
  	  	})

	var chartData2 = {
		labels : ['1~2 등급','ASDF','ASDF'],
	datasets : [
	{

		label : '1~2 등급',
	data : [ewglist[0]],
	datalabels:{
		color:'white',
	align: 'center',
	anchor: 'center'
		    	},
	backgroundColor : '#00ccff',
	borderWidth: 1
  					
  				},
	{


		label : '3~6 등급',
	data : [ewglist[1]],
	datalabels:{
		formatter: function (value, context) {
							if(value < 2){
								return "";
							}
		                  },
	color:'white',
	align: 'center',
	anchor: 'center'
			
			
			
				    },
	backgroundColor : '#FFCC66',
	borderWidth: 1
  					
  				},
	{

		label : '7~10 등급',
	data : [ewglist[2]],
	datalabels:{
		formatter: function (value, context) {
		                    
							if(value < 2){
								return "";
							}
		                    // 출력 텍스트
		                    
		                  },
	color:'white',                      // 배경색을 어떻게 세팅했냐에 따라 적절히..
	// pixel 단위이고, 수치로 입력
	align: 'center',
	anchor: 'center'
				      
	
			    	},
	backgroundColor : '#FF0000',
	borderWidth: 1
  					
  				},


	]
  		
  		};

	var chartOptions2 = {
		responsive:false,
	scales : {
		x: {
		stacked : true,
	display : false,
  				},
	y: {
		stacked : true,
	display : false,
  				},
  			},
	indexAxis : 'y',
	plugins : {
		legend : {
		display : true
  				}
  				
  			}
  		};


	// Age 차트

	if(agelist != 'None'){
		$(function() {
			var chartArea3 = document.getElementById('myChart3').getContext('2d');
			// 차트를 생성한다. 
			var myChart3 = new Chart(chartArea3, {
				type: 'bar',
				plugins: [ChartDataLabels],
				data: chartData3,
				options: chartOptions3

			})
		})
  	  	  	
  	  	  	var chartData3 = {
		labels : ['10대','20대','30대','40대','50대','60대'],
	datasets : [
	{



		data : [agelist[0], agelist[1], agelist[2], agelist[3], agelist[4], agelist[5]],
	datalabels:{
		// 너무 흐리다 싶어서 잘 보이도록 완전히 검게..
		color:'black',                      // 배경색을 어떻게 세팅했냐에 따라 적절히..
	// pixel 단위이고, 수치로 입력
	align: 'bottom',
	anchor: 'end',
	formatter: function (value, context) {
				                    var idx = context.dataIndex; // 각 데이터 인덱스
									if(value > 1){
										return value + '%';
									}else{
										return "";
									}
				                    // 출력 텍스트
				                    
				                  }
				
				
					    },
	backgroundColor : [
	'rgba(255, 99, 132, 0.2)',
	'rgba(54, 162, 235, 0.2)',
	'rgba(255, 206, 86, 0.2)',
	'rgba(75, 192, 192, 0.2)',
	'rgba(153, 102, 255, 0.2)',
	'rgba(255, 159, 64, 0.2)'

	],
	borderColor :  [
	'rgba(255, 99, 132, 1)',
	'rgba(54, 162, 235, 1)',
	'rgba(255, 206, 86, 1)',
	'rgba(75, 192, 192, 1)',
	'rgba(153, 102, 255, 1)',
	'rgba(255, 159, 64, 1)'

	],
	borderWidth : 1,
	borderRadius: 5,
  	  					
  	  				}


	]
  	  		
  	  		};

	var chartOptions3 = {
		plugins: {
		legend: {
		display: false
  	                  
  	              },
	title: {
		display: true,
	text: '연령별 인기도'
  	            }
  	          }
  	  		};
  		}

	if(sexlist != 'None'){
		$(function() {
			var chartArea4 = document.getElementById('myChart4').getContext('2d');
			// 차트를 생성한다. 
			var myChart4 = new Chart(chartArea4, {
				type: 'doughnut',
				plugins: [ChartDataLabels],
				data: chartData4,
				options: chartOptions4

			})
		})
  	  	  	
  	  	  	var chartData4 = {
		labels : ['여성','남성'],
	datasets : [
	{

		label : '성별 인기도',

	data : [sexlist[0], sexlist[1]],
	datalabels:{
		// 너무 흐리다 싶어서 잘 보이도록 완전히 검게..
		color:'white',                      // 배경색을 어떻게 세팅했냐에 따라 적절히..
	// pixel 단위이고, 수치로 입력
	align: 'center',
	anchor: 'center',
	formatter: function (value, context) {
				                    var idx = context.dataIndex; // 각 데이터 인덱스

	// 출력 텍스트
	return value + '%';
				                  }
				
				
					    },
	backgroundColor : ['#ff3300','#33ccff'],

	borderWidth : 1
  	  				}


	]
  	  		
  	  		};

	var chartOptions4 = {

	};
  		}


</script>
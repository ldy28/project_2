package com.example.entity;

import lombok.Data;

@Data
public class PageMaker {
	private Criteria cri;
	private int totalCount; // 총 게시글의 수
	private int startPage; // 시작 페이지 번호
	private int endPage; // 끝 페이지 번호
	private boolean prev;
	private boolean next;
	private int display=5;
	
	public void setTotalCount(int totalCount) {
		this.totalCount=totalCount;
		calcPaging();
	}

	private void calcPaging() {
		// 1. 화면에 보여질 마지막 페이지 번호
		endPage = (int)(Math.ceil(cri.getPage()/(double)display)*display);
		
		// 2. 시작 페이지 번호
		startPage = (endPage-display)+1;
		if(startPage<=0) startPage =1;
		
		// 3. 마지막 페이지 번호 계산
		int tempEndPage = (int)(Math.ceil(totalCount/(double)cri.getPerPageNum()));
		
		// 4. 화면에 보여질  마지막 페이지가 유효성 체크 
		if(endPage>tempEndPage) endPage=tempEndPage;
		if(endPage==0) endPage=1;
		
		// 5. 이전 페이지버튼 존재 체크
		prev = (startPage==1) ? false : true;
		
		// 6. 다음 페이지버튼 존재 체크
		next = (endPage<tempEndPage) ? true : false;
	}
	
	
}

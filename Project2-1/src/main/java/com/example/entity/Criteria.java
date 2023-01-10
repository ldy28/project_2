package com.example.entity;
import lombok.Data;

@Data
public class Criteria {
	private int page;	 //현재 페에지 번호
	private int perPageNum;
	private String skintype;
	private String typeEwg;
	private String keyword;
	private String typeChar;
	private String typeBrand;
	private String typeStar;
	private String typeReview;
	private String typeDate;
	private String manager;
	private String btnVal;
	private String memid;
	private String productType;
	
	
	
	public Criteria() {
		this.page = 1;
		this.perPageNum = 12;
		
	}
	
	// 현재 페이지의 게시글 시작 번호
	public int getPageStart() {
		return (page - 1) * perPageNum;
	}
}

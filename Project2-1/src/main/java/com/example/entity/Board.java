package com.example.entity;

import java.sql.Timestamp;

import lombok.Data;

@Data

public class Board {
	// 글 번호 
    private int boardSeq;

    // 글 제목 
    private String boardTitle;

    // 글 내용 
    private String boardContent;

    // 글 작성일자 
    private Timestamp boardDate;

    // 글 작성자 
    private String memID;

    // 글 조회수 
    private int boardCnt;

	
}

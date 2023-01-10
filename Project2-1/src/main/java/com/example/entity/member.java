package com.example.entity;

import java.sql.Timestamp;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Data
@NoArgsConstructor
public class member {
	// 회원 아이디
	@NonNull
	private String memID;
	// 회원 비밀번호
	@NonNull
	private String memPw;
	// 회원 이름
	@NonNull
	private String memName;
	// 회원 번호
	private String memPhone;
	// 회원 유형
	private String memType;
	// 회원가입일자
	private Timestamp memJoindate;

	
	
}

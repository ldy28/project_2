package com.example.mapper;

import java.util.List;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import com.example.entity.Criteria;
import com.example.entity.member;

@Mapper
public interface MemberMapper {

	
	@Select("select * from member where memID = #{memID}")
	public member idCheck(String memID);
	
	
	
	
	/*회원가입*/
	public void memberJoin(member member);

	public void signInsert(member vo);
	
	/*로그인*/
	public member getLogin(member vo);
	
	/*회원 정보 수정*/
	public void memberUpdate(member vo);
	
	/*관리자 페이지*/
	public List<member> memberList(Criteria cri);
	
	public int memberCount(Criteria cri);

	public void memDelete(String memID);

	public void memUpdate(String memID);
	
}

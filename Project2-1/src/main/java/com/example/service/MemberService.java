package com.example.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.entity.Criteria;
import com.example.entity.member;
import com.example.mapper.MemberMapper;
@Service
public class MemberService {


	@Autowired
	MemberMapper memberMapper;
	
	public void signInsert(member vo) {
		memberMapper.signInsert(vo);
	}
	
	public member loginCheck(member vo) {
		member mvo = memberMapper.getLogin(vo);
		return mvo;
	}
	// 멤버 업데이트
	public void memberUpdate(member vo) {
		memberMapper.memberUpdate(vo);
	}
	

	// 관리자 페이지 
	public List<member> memberList(Criteria cri) {
		if(cri.getBtnVal() != null) {
			if(cri.getBtnVal().equals("edit")) {
				memberMapper.memUpdate(cri.getMemid());
				
			}else if(cri.getBtnVal().equals("reject")) {
				memberMapper.memDelete(cri.getMemid());
				
			}
		}
		List<member> list = memberMapper.memberList(cri);

		return list;
	}
	public int memberCount(Criteria cri) {
		
		return memberMapper.memberCount(cri);
	}

	


}


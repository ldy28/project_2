package com.example.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.entity.Board;
import com.example.entity.Criteria;
import com.example.mapper.CosmeticMapper;

@Service
public class BoardService {
	@Autowired
	CosmeticMapper cosmeticMapper;

	public List<Board> allList(Criteria cri) {
		
		return cosmeticMapper.list(cri);
	}

	public int countBoard(Criteria cri) {
		// TODO Auto-generated method stub
		return cosmeticMapper.countBoard(cri);
	}
	
}

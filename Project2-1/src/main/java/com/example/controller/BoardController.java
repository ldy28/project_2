package com.example.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import com.example.entity.Board;
import com.example.entity.Criteria;
import com.example.entity.PageMaker;
import com.example.service.BoardService;

@Controller
public class BoardController {
	@Autowired
	BoardService boardService;
	@RequestMapping("/boardList.do")
	public String boardList(Model model,Criteria cri) {
		
		List<Board> list = boardService.allList(cri);
		model.addAttribute("boardList",list);
	    
		
		PageMaker pageMaker = new PageMaker();
		pageMaker.setCri(cri);
		pageMaker.setTotalCount(boardService.countBoard(cri));
		model.addAttribute("pageMaker",pageMaker);
		
		return "th/boardList";
	}
}

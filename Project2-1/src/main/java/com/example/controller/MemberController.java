package com.example.controller;

import java.util.List;

import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.example.entity.Criteria;
import com.example.entity.PageMaker;
import com.example.entity.member;
import com.example.mapper.MemberMapper;
import com.example.service.MemberService;

import lombok.RequiredArgsConstructor;
//RestController  //data
@Controller  //view
public class MemberController {
	
	@Autowired
	private MemberMapper mapper;
	@Autowired
	private MemberService service;
	
	
	/*
	 *  회원가입 페이지 이동
	 */
	@RequestMapping("/signup.do")
	public String signup() {
		return "th/signup";
	}
	
	/*
	 * 로그인 페이지 이동 */
	@GetMapping("/login.do")
	public String login() {
		return "th/login";
	}
	
	/*
	 *  아이디 중복체크
	 */
	@RequestMapping("/idCheck.do")
	public @ResponseBody member idCheck(String memID) {
			
		member vo =mapper.idCheck(memID);	
		
		if(vo != null) {
			vo = new member();
			vo.setMemID("true");
		}else {
			vo = new member();
			vo.setMemID("null");
		}
		return vo;
	}
	
	/*
	 *  회원가입시 로그인 페이지로 이동
	 */
	@PostMapping("/signup.do")
	public String signupForm(member vo) {
		service.signInsert(vo);
		return "th/login";
	}
	/*
	 *  회원가입 승인 후 로그인이 성공하면 메인 페이지로 이동
	 *  거부된 회원정보 or 틀린 정보로 로그인 시 로그인 페이지 리다이렉트
	 */
	@PostMapping("/login.do")
	public String loginCheck(member vo, HttpSession session, RedirectAttributes rttr) {
		member mvo = service.loginCheck(vo);
		if(mvo!=null) {
			session.setAttribute("mvo", mvo);
		}else {
			session.setAttribute("mvo", null);
			rttr.addFlashAttribute("msg", false);
			return "redirect:/login.do";
		}

		return "th/main";
	}
	/*
	 * 회원정보 수정페이지로 이동
	 * */
	@RequestMapping("/memberUpdateView.do")
	public String memberUpdate() {
		return "th/memberUpdateView";
	}
	
	/*
	 *  회원정보 수정
	 */
	@PostMapping("/memberUpdate.do")
	public String memberUpdate(member vo, HttpSession session) {
		service.memberUpdate(vo);
		session.invalidate();
		return "redirect:/main.do";
	}
	
	/*
	 *  관리자 페이지
	 */
	@RequestMapping("/memberList.do")
	public String memberList(Model model, Criteria cri){
		if(cri.getManager() == null) cri.setManager("recognize");
		List<member> list = service.memberList(cri);
		model.addAttribute("memberList",list);
		
		System.out.println(cri);
		PageMaker pageMaker = new PageMaker();
		
		pageMaker.setCri(cri);
		pageMaker.setTotalCount(service.memberCount(cri));
		System.out.println(pageMaker.getStartPage());
		System.out.println(pageMaker.getEndPage());
		model.addAttribute("pageMaker",pageMaker);
		return "th/manager";
	}
	/*
	 *  로그아웃 버튼 클릭 시 로그인 페이지로 이동
	 */
	@RequestMapping("/logout.do")
	public String loginOut(HttpSession session) {
		session.invalidate(); //무효화
		return "redirect:/login.do";
	}
	

}


		
	
	
	


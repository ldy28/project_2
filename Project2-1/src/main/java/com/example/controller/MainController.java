package com.example.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.devtools.restart.RestartScope;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.service.MainService;

@Controller
public class MainController {
	@Autowired
	MainService mainService;
	
	@RequestMapping("/main.do")
	public String main() {
		return "th/main";
	}
}

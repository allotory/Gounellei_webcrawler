package com.crawler.zhihu.model;

import java.util.ArrayList;
import java.util.List;

public class Zhihu {
	
	private String question;
	private String quesDescription;
	private String url;
	private List<String> answers;
	
	public Zhihu(){
		question = "";
		quesDescription = "";
		url = "";
		answers = new ArrayList<String>();
	}

	@Override
	public String toString() {
		return "问题：" + question +"\r\n描述：" + quesDescription + "\r\n链接：" 
					+ url + "\r\n答案：" + answers + "\r\n";
	}

	public String getQuestion() {
		return question;
	}

	public void setQuestion(String question) {
		this.question = question;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public List<String> getAnswers() {
		return answers;
	}

	public void setAnswers(List<String> answers) {
		this.answers = answers;
	}

	public String getQuesDescription() {
		return quesDescription;
	}

	public void setQuesDescription(String quesDescription) {
		this.quesDescription = quesDescription;
	}
}

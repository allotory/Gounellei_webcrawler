package com.crawler.zhihu.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.crawler.zhihu.model.Zhihu;

public class Crawler {
	public String getPage(String url) {
		// 定义一个字符串用来存储网页内容
		String page = "";
		// 定义一个缓冲字符输入流 
		BufferedReader reader = null;

		try {
			// 将string转成url对象
			URL urlObject = new URL(url);
			// 初始化一个链接到那个url的连接
			URLConnection connection = urlObject.openConnection();
			connection.setRequestProperty("User-Agent",
					"Mozilla/4.0 (compatible; MSIE 5.0; Windows NT; DigExt)");
			// 开始实际的连接
			connection.connect();
			// 初始化 BufferedReader输入流来读取URL的响应
			reader = new BufferedReader(new InputStreamReader(
					connection.getInputStream()));
			// 用来临时存储抓取到的每一行的数据
			String line = "";
			while ((line = reader.readLine()) != null) {
				page += line;
			}
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (reader != null) {
					reader.close();
				}
			} catch (Exception ex) {
				ex.printStackTrace();
			}
		}
		return page;
	}
	
	public List<Zhihu> RegexString(String page){
		//list存储主题列表
		List<Zhihu> zhihuList = new ArrayList<Zhihu>();
		//获取到URL
		Pattern urlPattern = Pattern.compile("<h2>.+?question_link.+?href=\"(.+?)\".+?</h2>");
		Matcher urlMatcher = urlPattern.matcher(page);
		//System.out.println(page);
		//是否匹配成功
		boolean isFind = urlMatcher.find();
		while (isFind){
			Zhihu zh = new Zhihu();
			zh.setUrl(RealURL.getRealURL(urlMatcher.group(1)));
			//System.out.println(urlMatcher.group(1) + "====" + RealURL.getRealURL(urlMatcher.group(1)));
			//zh.setUrl(urlMatcher.group(1));
			//System.out.println(urlMatcher.group(1));
			zhihuList.add(zh);
			isFind = urlMatcher.find();
		}
		return zhihuList;
	}
	
	public List<Zhihu> getQuestion(List<Zhihu> zhihuList){
		
		List<Zhihu> zhihuListFull = new ArrayList<Zhihu>();
	
		//遍历列表分别处理每一个问题
		for(Zhihu zhihu : zhihuList){
			//读取问题页面
			String page = this.getPage(zhihu.getUrl());
			//System.out.println(zhihu.getUrl());
			//匹配对象
			Pattern pattern = null;  
            Matcher matcher = null;
            //匹配标题
            pattern = Pattern.compile("zm-item-title zm-editable-content\">(.*?)</h2>");  
            matcher = pattern.matcher(page);  
            if (matcher.find()) {  
                zhihu.setQuestion(matcher.group(1));;  
            }  
            //匹配问题内容
            pattern = Pattern.compile("<div class=\"zm-editable-content\">(.*?)</div>");
            matcher = pattern.matcher(page);
            if (matcher.find()) {
            	zhihu.setQuesDescription(matcher.group(1));
            }
            
            zhihuListFull.add(zhihu);
		}
		
		return zhihuListFull;
	}

	public static void main(String args[]) {
		// 定义即将访问的链接
		String url = "http://www.zhihu.com/explore/recommendations";
		Crawler c = new Crawler();
		String page = c.getPage(url);
		List<Zhihu> zhihuList = c.RegexString(page);
		List<Zhihu> zhihuListFull = c.getQuestion(zhihuList);
		System.out.println(zhihuListFull);
	}
}
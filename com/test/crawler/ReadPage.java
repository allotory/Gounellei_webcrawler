package com.test.crawler;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ReadPage {
	public String getPage(String url) {
		// 定义一个字符串用来存储网页内容
		String result = "";
		// 定义一个缓冲字符输入流 
		BufferedReader reader = null;

		try {
			// 将string转成url对象
			URL urlObject = new URL(url);
			// 初始化一个链接到那个url的连接
			URLConnection connection = urlObject.openConnection();
			// 开始实际的连接
			connection.connect();
			// 初始化 BufferedReader输入流来读取URL的响应
			reader = new BufferedReader(new InputStreamReader(
					connection.getInputStream()));
			// 用来临时存储抓取到的每一行的数据
			String line = "";
			while ((line = reader.readLine()) != null) {
				result += line;
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
		return result;
	}
	
	static String RegexString(String targetStr, String patternStr){
		Pattern pattern = Pattern.compile(patternStr);
		Matcher matcher = pattern.matcher(targetStr);
		if (matcher.find()){
			return matcher.group(1);
		}
		return "";
	}

	public static void main(String args[]) {
		// 定义即将访问的链接
		String url = "http://www.baidu.com/";
		ReadPage gb = new ReadPage();
		String result = gb.getPage(url);
		String imgsrc = RegexString(result, "src=\"(.+?)\"");
		System.out.println(result);
		System.out.println(imgsrc);
	}
}
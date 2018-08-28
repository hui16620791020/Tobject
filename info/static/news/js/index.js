var currentCid = 1; // 当前分类 （1 最新）
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // true:表示正在请求数据 false：没有在请求数据


$(function () {

    // 获取首页新闻数据
    updateNewsData()

    // 首页分类切换
    $('.menu li').click(function () {

        // 获取分类id值
        var clickCid = $(this).attr('data-cid')

        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        // 将当前点击的分类激活
        $(this).addClass('active')

        // 6 != 2 切换分类了
        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            // 请求数据
            updateNewsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // TODO 判断页数，去更新新闻数据
            // data_querying: false 表示没有人在加载数据
            // 拖动到尾部我们就可以再去请求下一页的数据
            if(!data_querying){

                cur_page += 1
                // 保证当前页面小于总页数
                if(cur_page < total_page){
                     //请求数据
                    data_querying = true
                    updateNewsData()
                }else{
                    // 页码超出总数的也不能去加载数据
                    data_querying = true

                }
            }
        }
    })
})

function updateNewsData() {
    // TODO 更新新闻数据
    params = {
        "cid": currentCid,
        "page": cur_page

    }
    $.get("/news_list",params, function (resp) {
        if(resp.errno == "0"){
            // 获取首页新闻数据成功
            // 给总页数赋值
            total_page = resp.data.total_page
            // 0. 数据请求完毕
            data_querying = false
            // 1. 清空之前数据(只有第一页的数据才需要清除)
            if(cur_page == 1) {
                $(".list_con").html('')
            }
            // 2. 显示数据
            for (var i=0;i<resp.data.newsList.length;i++) {
                var news = resp.data.newsList[i]
                var content = '<li>'
                content += '<a href="/news/'+ news.id +'" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>'
                content += '<a href="/news/'+ news.id +'" class="news_title fl">' + news.title + '</a>'
                content += '<a href="/news/'+ news.id +'" class="news_detail fl">' + news.digest + '</a>'
                content += '<div class="author_info fl">'
                content += '<div class="source fl">来源：' + news.source + '</div>'
                content += '<div class="time fl">' + news.create_time + '</div>'
                content += '</div>'
                content += '</li>'
                $(".list_con").append(content)
            }

        }

    })

}

import java.sql.Connection
import java.sql.DriverManager
import java.sql.ResultSet
import java.sql.SQLException
import java.sql.Statement

/**
 * Created by qcl on 2017/11/18.
 * 数据库连接
 */

object DB {
    @JvmStatic
    fun main(args: Array<String>) {
        val con: Connection
        val driver = "com.mysql.jdbc.Driver"
        //这里我的数据库是qcl
        val url = "jdbc:mysql://localhost:3306/qcl"
        val user = "root"
        val password = "qcl123"
        try {
            Class.forName(driver)
            con = DriverManager.getConnection(url, user, password)
            if (!con.isClosed) {
                println("数据库连接成功")
            }
            val statement = con.createStatement()
            val sql = "select * from home;"//我的表格叫home
            val resultSet = statement.executeQuery(sql)
            var name: String
            while (resultSet.next()) {
                name = resultSet.getString("name")
                println("姓名：$name")
            }
            resultSet.close()
            con.close()
        } catch (e: ClassNotFoundException) {
            println("数据库驱动没有安装")

        } catch (e: SQLException) {
            println("数据库连接失败")
        }

    }
}
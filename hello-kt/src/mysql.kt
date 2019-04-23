import java.sql.Connection
import java.sql.DriverManager
import java.sql.ResultSet
import java.sql.SQLException
import java.sql.Statement

/**
 * Created by sand on 2019/4/6.
 * 数据库连接
 */

object DB {
    @JvmStatic
    fun main(args: Array<String>) {
        val con: Connection
        val driver = "com.mysql.cj.jdbc.Driver"
        //这里是数据库
        //val url = "jdbc:mysql://db4free.net:3306/baoxianjihuashu?serverTimezone=UTC&useUnicode=true&characterEncoding=utf8&characterSetResults=utf8&useSSL=false&verifyServerCertificate=false&autoReconnct=true&autoReconnectForPools=true&allowMultiQueries=true"
        val url = "jdbc:mysql://db4free.net:3306/baoxianjihuashu?useSSL=false&serverTimezone=UTC"
        val user = "sandorn"
        val password = "eeM3sh4KPkp4sJ8A"
        try {

            Class.forName(driver)
            con = DriverManager.getConnection(url, user, password)
            if (!con.isClosed) {
                println("数据库连接成功")
            }
            val statement = con.createStatement()
            var sql = "select table_name from information_schema.tables "
            var resultSet = statement.executeQuery(sql)

            while (resultSet.next()) {
                println(resultSet.getString("费率"))
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
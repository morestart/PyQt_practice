from os import popen
from pathlib import Path


def dir_is_valid(dir_p) -> bool:
    """验证有效性：只有以2位数字开头的文件夹才是需要的"""
    return dir_p.name[0:2].isdigit()


def file_is_valid(file_p) -> bool:
    """验证有效性：根据本项目命名规律，所有.py或.md文件才是需要目录的"""
    return file_p.suffix in (".py", ".md")


class TocMaker:
    """
    生成项目toc目录、统计代码行数并写入markdown文件
    """

    def __init__(self, working_dir: str = "./"):
        self.working_dir = Path(working_dir)
        self.tree_dict = None
        self.cloc_result = None
        self.tree()

    def tree(self):
        """
        列出工作目录下所有符合要求的目录和文件
        """
        tree_result = dict()
        file_name_list = list()

        # 列出工作目录下所有项目并验证有效性：只有以2位数字开头的文件夹才是需要的
        valid_dir_list = [
            x for x in self.working_dir.iterdir() if x.is_dir() and dir_is_valid(x)
        ]
        valid_dir_list.sort()  # 按照名称排序

        # 验证有效性
        for valid_dir in valid_dir_list:
            iterated_files = list(valid_dir.iterdir())
            iterated_files.sort()
            for file in iterated_files:
                # 根据本项目命名规律，所有.py或.md文件才是需要目录的
                if file_is_valid(file):
                    file_name_list.append(file)
            tree_result.update({valid_dir: file_name_list})
            file_name_list = list()  # 重新置空

        self.tree_dict = tree_result

    def cloc(self, gitignore_file: str = ".gitignore"):
        """
        使用cloc统计项目代码行数
        """
        ignored_dir = ""
        gitignore_file_p = Path(gitignore_file)
        with gitignore_file_p.open("r", encoding="UTF-8") as f:
            for dir_name in f.readlines():
                dir_name = dir_name.replace("/", "")
                dir_name = dir_name.replace("\n", ",")
                ignored_dir += dir_name

        # 调用cloc，并排除gitignore中的目录，需要提前将cloc添加到系统环境变量
        cmd = f"cloc --exclude-dir {ignored_dir} {str(self.working_dir)}"

        with popen(cmd) as p:
            cmd_result = p.read()
            # 如果cmd执行正常退出则p.close()返回None，失败则返回状态码
            if p.close():
                print("cloc调用失败，请检查")
            else:
                # 根据cloc返回结果，连续两个换行符后面的内容是需要的信息
                self.cloc_result = cmd_result.split("\n\n", 1)[1]
                print(self.cloc_result)

    def write_into_md(self, toc_file="./toc.md"):
        """
        把目录和文件名写入toc.md文件
        """
        write_lines = list()
        file_counter = 0
        toc_file_p = Path(toc_file)

        if self.tree_dict:
            for dir_name in self.tree_dict:
                list_counter = 0
                write_lines.append(
                    f"### {dir_name.name[:2]} [{dir_name.name[3:]}](./{dir_name.name})\n\n"
                )
                for file_name in self.tree_dict[dir_name]:
                    write_lines.append(
                        f"{list_counter}. [{file_name.name[3:]}](./{file_name.as_posix()})\n\n"
                    )
                    file_counter += 1
                    list_counter += 1
            counter_info = f"共{len(self.tree_dict)}个目录，{file_counter}个文件."  # 计数器
            write_lines += counter_info
            with toc_file_p.open("wt", encoding="UTF-8") as f:
                f.writelines(write_lines)
            print(f"TOC生成成功，{counter_info}")
        else:
            print("tree列表为空，请检查")


if __name__ == "__main__":
    toc_maker = TocMaker("./")
    toc_maker.write_into_md("./toc.md")
    toc_maker.cloc()  # 需要在系统中安装cloc并且把命令 'cloc' 添加到环境变量，否则注释掉本行

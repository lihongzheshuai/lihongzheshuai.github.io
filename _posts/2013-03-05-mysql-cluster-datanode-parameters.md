---
layout: post
title: MySQL Cluster Data Node配置参数列表及说明
date: 2013-03-05 13:38 +0800
author: onecoder
comments: true
tags: [MySQL]
thread_key: 1368
---
<ul>
	<li>
		<span >Id</span></li>
</ul>
<div >
	<table border="1" >
		<colgroup>
			<col />
			<col />
			<col />
			<col />
		</colgroup>
		<thead s>
			<tr >
				<th >
					Effective Version</th>
				<th >
					Type/Units</th>
				<th >
					Default</th>
				<th >
					Range/Values</th>
			</tr>
		</thead>
		<tbody s>
			<tr >
				<td >
					NDB 7.2.0</td>
				<td >
					unsigned</td>
				<td >
					[none]</td>
				<td >
					1 - 48</td>
			</tr>
			<tr >
				<td colspan="4" >
					<span >Restart Type:</strong></span>&nbsp;N</td>
			</tr>
		</tbody>
	</table>
	集群内部节点的唯一标识，取值范围从1-48。目前被废弃，建议用NodeId替换。</div>
<div >
	<ul>
		<li>
			ExecuteOnComputer</li>
	</ul>
	<div>
		<table border="1" style="margin: 0px 0px 10px; padding: 0px; border: none; outline: 0px; font-size: 14px; vertical-align: baseline; background-color: rgb(255, 255, 255); border-spacing: 0px; border-collapse: collapse; max-width: 660px; font-family: Helvetica, Arial, sans-serif; line-height: 16px;" summary="This table provides type and value information for the ExecuteOnComputer data node configuration parameter">
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						name</td>
					<td >
						[none]</td>
					<td >
						...</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;S</td>
				</tr>
			</tbody>
		</table>
		在[computer]章节配置。值指向配置过的Id。用于指定节点运行的主机。</div>
</div>
<div >
	<ul>
		<li>
			HostName</li>
	</ul>
	<div>
		<table border="1" >
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						name or IP address</td>
					<td >
						localhost</td>
					<td >
						...</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;S</td>
				</tr>
			</tbody>
		</table>
		用于指定data节点运行的主机。值配置主机名或者IP。默认值为localhost。该参数和ExecuteOnComptuter作用相同。</div>
</div>
<div >
	<ul>
		<li>
			ServerPort</li>
	</ul>
	<div>
		<table border="1" >
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						unsigned</td>
					<td >
						[none]</td>
					<td >
						1 - 64K</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;N</td>
				</tr>
			</tbody>
		</table>
		集群中的每个节点需要一个端口跟其他节点通信。默认该参数的值是动态生成，一保证在同一个计算机上的多个节点不会使用同一个端口号。所以，一般不设置该值。该值在[ndbd]章节配置。</div>
</div>
<div >
	<ul>
		<li>
			NodeGroup</li>
	</ul>
	<div>
		<table border="1" >
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						&nbsp;</td>
					<td >
						[none]</td>
					<td >
						0 - 65536</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;IS</td>
				</tr>
			</tbody>
		</table>
		用于将data节点分配到指定的NodeGroup中。在集群初次启动后该参数是只读的，并且不能用于在线重新分配数据节点。</div>
</div>
<div >
	&nbsp;</div>
<div >
	该参数主要用来在运行的MySQL集群中添加新的node group，而不用滚动重启。建议在以后考虑添加到集群的节点上设置该值。建议65536。</div>
<div >
	<ul>
		<li>
			NoOfReplicas</li>
	</ul>
	<div>
		<table border="1" >
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						integer</td>
					<td >
						2</td>
					<td >
						1 - 4</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;IS</td>
				</tr>
			</tbody>
		</table>
		全局设置，仅可以设置在[ndbd default]配置段。用于指定表数据在集群中复制的份数。同时也指定了node group中的节点数。一个node group是一组保存相同信息的节点群。因此，同一个node group的节点，尽量不要运行在同一个计算机上，以免单点故障造成数据丢失。</div>
</div>
<div >
	&nbsp;</div>
<div >
	该参数最大值为4，不过目前只有1，2是实际支持的。</div>
<div >
	<ul>
		<li>
			DataDir</li>
	</ul>
	<div>
		<table border="1" >
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						path</td>
					<td >
						.</td>
					<td >
						...</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;IN</td>
				</tr>
			</tbody>
		</table>
		指定trace文件,log文件,pid文件和错误日志的存放位置。默认是data节点进程的工作目录。</div>
</div>
<div >
	<ul>
		<li>
			FileSystemPath</li>
	</ul>
	<div>
		<table border="1" >
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						path</td>
					<td >
						DataDir</td>
					<td >
						...</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;IN</td>
				</tr>
			</tbody>
		</table>
		用于指定保存metadata,REDO日志, UNDO日志(用于磁盘存储表), 数据文件的保存路径。默认值为DataDir指定的值。</div>
</div>
<div >
	<ul>
		<li>
			BackupDataDir</li>
	</ul>
	<div>
		<table border="1" >
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						path</td>
					<td >
						[see text]</td>
					<td >
						...</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;IN</td>
				</tr>
			</tbody>
		</table>
		备份文件保存路径。</div>
</div>
<div >
	<ul>
		<li>
			<b><font color="#E30000">Data Memory</font></b></li>
	</ul>
	<div>
		<table border="1" >
			<colgroup>
				<col />
				<col />
				<col />
				<col />
			</colgroup>
			<thead s>
				<tr >
					<th >
						Effective Version</th>
					<th >
						Type/Units</th>
					<th >
						Default</th>
					<th >
						Range/Values</th>
				</tr>
			</thead>
			<tbody s>
				<tr >
					<td >
						NDB 7.2.0</td>
					<td >
						bytes</td>
					<td >
						80M</td>
					<td >
						1M - 1024G</td>
				</tr>
				<tr >
					<td colspan="4" >
						<span >Restart Type:</strong></span>&nbsp;N</td>
				</tr>
			</tbody>
		</table>
		定义用于存储数据的内存空间。所以一定要保证有足够的物理内存。</div>
</div>
<div >
	&nbsp;</div>
<div >
	分配给DataMemory的内存空间同时保存实际数据和索引。每条记录有16byte的开销。此外，每条记录还需要额外的空间，因为记录保存在具有128byte页面开销的32kb页中。每个页面有少量的浪费，因为每条记录仅保存在 一个页面中。</div>
<div >
	&nbsp;</div>
<div >
	对于变长的字段，数据保存DataMemory定义的在不同数据页面中。变长的字段也使用定长保存，额外使用4字节指向变长部分。变长部分，有2byte开销另外加上每个属性2字节。</div>
<div >
	&nbsp;</div>
<div >
	最大的记录大小为14000字节。</div>
<div >
	&nbsp;</div>
<div >
	DataMemory定义的内存空间同样也用于保存有序索引，使用约10byte每字节。表中的每行数据都表现在有序索引中。用户常错误的认为所有的索引都保存的IndexMemeory定义的内存中，实际上只有主键和唯一hash索引使用IndexMemory; 有序索引使用DataMemory分配的内存空间。然而，在创建逐渐或者唯一hash索引的时候同时也在该键上创建一个有序索引。除非你在创建索引的时候显示指定USING HASH。可以通过ndb_desc -d dbname_table_name查看详情。</div>
<div >
	&nbsp;</div>
<div >
	目前，每个分区最大hash索引容量为512MB。</div>
<div >
	&nbsp;</div>
<div >
	DataMemory同样保存UNDO信息。每次更新的未变化的数据的副本保存的DataMemory中。同事还有每个副本的引用在有序索引中。只有数据插入事物调后，旧数据的备份才会删除，因此大事物需要更多的内存空间。</div>
<div >
	&nbsp;</div>
<div >
	<ul>
		<li>
			大事物比小事物慢</li>
		<li>
			大事物增加事物失败时丢失并重新执行的了操作数。</li>
		<li>
			大事物使用更多的内存。</li>
	</ul>
	<div>
		<hr />
		注：在翻译和总结到这里的时候<a href="http://www.coderli.com">OneCoder</a>发现了一个网站上对文档翻译总结相当不错：</div>
	<div>
		<a href="http://doc.javanb.com/mysql-5-1-reference-manual-zh/ndbcluster.html#mysql-cluster-config-file">http://doc.javanb.com/mysql-5-1-reference-manual-zh/ndbcluster.html#mysql-cluster-config-file</a>&nbsp;，所以决定对下面的部分，直接转载，自己也顺便学习一下。(注：转载是的翻译是基于MySQL5.1版本的集群，现在是5.5版本的)</div>
	<div>
		&nbsp;</div>
	<div>
		IndexMemory</div>
</div>
<div >
	&nbsp;</div>
<div >
	<table border="1" style="margin: 0px 0px 10px; padding: 0px; border: none; outline: 0px; font-size: 14px; vertical-align: baseline; background-color: rgb(255, 255, 255); border-spacing: 0px; border-collapse: collapse; max-width: 660px; font-family: Helvetica, Arial, sans-serif; line-height: 16px;" summary="This table provides type and value information for the IndexMemory data node configuration parameter">
		<colgroup>
			<col />
			<col />
			<col />
			<col />
		</colgroup>
		<thead s>
			<tr >
				<th >
					Effective Version</th>
				<th >
					Type/Units</th>
				<th >
					Default</th>
				<th >
					Range/Values</th>
			</tr>
		</thead>
		<tbody s>
			<tr >
				<td >
					NDB 7.2.0</td>
				<td >
					bytes</td>
				<td >
					18M</td>
				<td >
					1M - 1T</td>
			</tr>
			<tr >
				<td colspan="4" >
					<span >Restart Type:</strong></span>&nbsp;N</td>
			</tr>
		</tbody>
	</table>
	<div>
		该参数用于控制MySQL簇中哈希（混编）索引所使用的存储量。哈希（混编）索引总用于主键索引、唯一性索引、以及唯一性约束。注意，定义主键和唯一性索引时，将创建两条索引，其中一条是用于所有tuple访问和锁定处理的哈希（混编）索引。此外，它还能用于增强唯一性约束。</div>
	<div>
		哈希（混编）索引的大小是每记录25字节，再加上主键的大小。对大于32字节的主键，还需加上8字节。</div>
	<div>
		考虑下例定义的表：</div>
	<blockquote>
		<div>
			CREATE TABLE example (</div>
		<div>
			&nbsp; a INT NOT NULL,</div>
		<div>
			&nbsp; b INT NOT NULL,</div>
		<div>
			&nbsp; c INT NOT NULL,</div>
		<div>
			&nbsp; PRIMARY KEY(a),</div>
		<div>
			&nbsp; UNIQUE(b)</div>
		<div>
			) ENGINE=NDBCLUSTER;</div>
	</blockquote>
	<div>
		有12字节的开销（无可空列将节省4字节的开销）加上每记录12字节的数据。此外，在列a和b上有两个有序索引，假定每记录分别耗用约10字节的空间。在每记录约使用29字节的基表上有1条主键哈希索引。唯一性约束由以b作为主键以及a作为列的单独表实现。对于该表，每记录将耗用额外的29字节索引内存，在示例表中，还包括12字节的开销再加上8字节的记录数据。</div>
	<div>
		因此，对于100万条记录，需要58MB的索引内存来处理用于主键和唯一性约束的哈希索引。还需要64 MB来处理基表和唯一索引表、以及两个有序索引表的记录。</div>
	<div>
		由此可见，哈希索引占用了相当大的内存空间，但作为回报，它们提供了对数据的极快访问。在MySQl簇中，它们也用于处理唯一性约束。</div>
	<div>
		目前仅有的分区算法是散列法，有序索引对每个节点来说都是局部性的。因此，有序索引不能用于处理一般情况下的唯一性约束。</div>
	<div>
		对于IndexMemory和DataMemory，重要的是，总的数据库大小是各节点组的所有数据内存和所有索引内存之和。每个节点组用于保存复制信息，因此，如果有4个节点和2个副本，将有2个节点组。对于每个数据节点，可用的总数据内存是2*DataMemory。</div>
	<div>
		强烈建议为所有的节点设置相同的DataMemory值和IndexMemory值。由于数据是平均分布在簇中的所有节点上，任何节点可用的最大空间不超过簇中最小节点的可用空间。</div>
	<div>
		DataMemory和IndexMemory可被更改，但降低任何一个的值均会导致危险，如果这样做，很容易使某一节点甚至整个簇因缺少足够的内存空间而无法重启。增加它们的值应是可接受的，但建议采用与软件升级相同的方式升级它，首先更新配置文件，然后重启管理服务器，最后依次重启每个数据节点。</div>
	<div>
		更新不会增加所用的索引内存。插入将立刻生效，但是，在提交事务之前并不会实际删除行。</div>
	<div>
		IndexMemory的默认值是18MB。最小值为1MB。</div>
	<div>
		&nbsp;</div>
	<div>
		<b>事务参数</b></div>
	<div>
		&nbsp;</div>
	<div>
		下面讨论的三个参数十分重要，这是因为，它们会影响并发事务的数目，以及系统能够处理的事务的大小。MaxNoOfConcurrentTransactions用于设置节点内可能的并发事务数目。MaxNoOfConcurrentOperations用于设置能同时出现在更新阶段或同时锁定的记录数目。</div>
	<div>
		对于打算设定特定值、不使用默认值的用户，这两个参数可能正是他们所需的（尤其是MaxNoOfConcurrentOperations）。默认值是为使用小型事务的系统而设置的，为的是确保这类事务不会使用过多的内存。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<b>&nbsp;[NDBD]MaxNoOfConcurrentTransactions</b></div>
	<div>
		对于簇中的每个活动事务，必须在簇节点之一中有1条记录。对事务的协调任务是在各节点间进行的：在簇中，事务记录的总数等于任意给定节点中的事务数乘以簇中的节点数。</div>
	<div>
		事务记录被分配给单独的MySQL服务器。正常情况下，对于使用簇中任何表的每个连接，必须为其分配至少1条事务记录。出于该原因，应确保簇中的事务记录数大于簇中所有MySQL服务器的并发连接数。</div>
	<div>
		对于所有的簇节点，必须将该参数设置为相同的值。</div>
	<div>
		更改该参数不安全，如果这样做，会导致簇崩溃。当某一节点崩溃时，簇中的一个节点（实际上是生存时间最久的节点）将为崩溃之时正在崩溃节点中运行的所有事务建立事务状态。因此，重要的是，该节点的事务记录数不低于失效节点中的事务记录数。</div>
	<div>
		该参数的默认值为4096。</div>
	<div>
		&nbsp;</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp;&nbsp;<b>&nbsp; [NDBD]MaxNoOfConcurrentOperations</b></div>
	<div>
		根据事务的大小和数目调整该参数的值，这个想法不错。执行仅包含少量操作且不涉及很多记录的事务时，不需要将该参数设置得很高。但在执行涉及大量记录的大事务时，需要将该参数设置得较高。</div>
	<div>
		对于每次事务更新的簇数据，均会保存记录，并会将它们保存在事务协调器中以及执行实际更新的节点中。这些记录包含所需的状态信息，这类信息可用于为回滚操作找到UNDO记录，用于锁定查询或其他目的。</div>
	<div>
		<font color="#E30000"><b>该参数应被设置为：事务中同时更新的记录数除以簇数据节点的数目。例如，在包含4个数据节点的簇中，如果预期处理的、使用事务的并发更新数为1000000，就应将该值设置为1000000 / 4 = 250000</b></font>。</div>
	<div>
		设置锁定的读请求也会导致操作记录的创建。在单独节点内也会分配一些额外的空间，以便处理在节点间分配不完美的问题。</div>
	<div>
		当查询使用唯一性哈希索引时，对于事务中的每条记录，实际上将使用两条操作记录。第1条记录代表在索引表中的读，第2条记录负责处理基表上的操作。</div>
	<div>
		该参数的默认值为32768.</div>
	<div>
		该参数实际上处理的是能分别配置的两个值。第1个值指定了将多少操作记录放到事务协调器中，第2个值指定了多少操作记录是数据库的本地记录。</div>
	<div>
		对于在8节点簇上执行的特大事务，它要求事务协调器中的操作记录数不少于事务中涉及的读取、更新和删除次数。然而，簇中的操作记录分布在所有的8个节点上。因此，如果有必要为特大事务配置系统，良好的方法是分别配置该参数的两个部分。MaxNoOfConcurrentOperations总会被用于计算节点的事务协调器部分中的操作记录数。</div>
	<div>
		应了解操作记录对内存的要求，这点也很重要。每记录约消耗1KB。</div>
	<div>
		&nbsp;</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<b>&nbsp;[NDBD]MaxNoOfLocalOperations</b></div>
	<div>
		默认情况下，将按照1.1 * MaxNoOfConcurrentOperations计算该参数，它适合于具有很多并发事务但不存在特大事务的系统。如果需要在某一时间处理特大事务而且有很多节点，最好通过明确指定该参数以覆盖默认值。</div>
	<div>
		&nbsp;</div>
	<div>
		<b>事务临时存储</b></div>
	<div>
		&nbsp;</div>
	<div>
		下一组参数用于决定执行作为簇事务组成部分的查询时所需的临时存储空间。查询完成后将释放所有记录，簇将等待提交或回滚事件。</div>
	<div>
		对于大多数情况，这些参数的默认值是恰当的。但是，如果需要支持涉及大量行或操作的事务，用户或许应增大这些参数的值，以便在系统中获得更好的平行性。对于需要相对较少事务的应用程序，用户可降低这些参数的值，以便节省内存。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<b>&nbsp;[NDBD]MaxNoOfConcurrentIndexOperations</b></div>
	<div>
		对于使用唯一性哈希索引的查询，在查询执行期间，将使用操作记录的另一个临时集合。该参数用于设置记录池的大小。因此，仅当执行查询的某一部分时才会分配该记录，一旦该部分执行完成，将释放记录。对于处理放弃和提交所需的状态，它是由正常的操作记录负责处理的，这类记录的池大小由参数MaxNoOfConcurrentOperations设置。</div>
	<div>
		该参数的默认值为8192。只有在极其罕见的情况下，需要使用唯一性哈希索引执行极高的并行操作时，才有必要增大该值。如果DBA（数据库管理员）确信该簇不需要高的并行操作，可以使用较小的值并节省内存。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;<b>[NDBD]MaxNoOfFiredTriggers</b></div>
	<div>
		MaxNoOfFiredTriggers的默认值是4000，它足以应付大多数情况。在某些情况下，如果DBA认为在簇中对并行操作的要求并不高，甚至还能降低它。</div>
	<div>
		执行会影响唯一哈希索引的操作时，将创建记录。在具有哈希索引的表中插入或删除记录时，或更新作为唯一哈希索引组成部分的列时，均会触发索引表中的插入或删除操作。所获得的记录用于代表该索引表操作，同时等待促使其完成的初始操作。该操作的时间很短，但对于在基表（包含唯一哈希索引）上有很多并发写操作的情形，仍需要在记录池中有大量的记录。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;<b>[NDBD]TransactionBufferMemory</b></div>
	<div>
		该参数影响的内存用于跟踪更新索引表和读取唯一索引时执行的操作。该内存用于保存关于这类操作的键和列信息。几乎不需要更改该参数的默认值。</div>
	<div>
		正常的读和写操作使用类似的缓冲区，其使用时间甚至更短。编译时间参数ZATTRBUF_FILESIZE（在ndb/src/kernel/blocks/Dbtc/Dbtc.hpp中）被设为4000*128字节（500KB）。用于 键信息的类似缓冲区，ZDATABUF_FILESIZE（也在Dbtc.hpp中）包含4000 * 16 = 62.5KB的缓冲空间。Dbtc是用于处理事务协调的模块。</div>
	<div>
		扫描和缓冲</div>
	<div>
		在Dblqh模块中（在ndb/src/kernel/blocks/Dblqh/Dblqh.hpp内）有很多附加参数，这些参数会影响读和写操作。这些参数包括：ZATTRINBUF_FILESIZE，默认值为10000*128字节（1250KB）；以及ZDATABUF_FILE_SIZE，默认的缓冲空间大小为10000*16字节（约156KB）。到目前为止，没有任何迹象表明应增加这类编译时间限制参数的值，无论是用户报告还是我们自己的大量测试。</div>
	<div>
		TransactionBufferMemory的默认值是1MB。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;<b>[NDBD]MaxNoOfConcurrentScans</b></div>
	<div>
		该参数用于控制可在簇中执行的并行扫描的数目。每个事务协调程序均能处理为该参数定义的并行扫描。对于每次执行的扫描查询，将以并行方式扫描所有分区。每次分区扫描将使用分区所在节点内的扫描记录，记录数等于该参数的值乘以节点数。簇应能支持从簇内所有节点同时执行的MaxNoOfConcurrentScans扫描。</div>
	<div>
		扫描实际上是在两种情况下执行的。第1种情况是，处理查询时不存在哈希或有序索引，在该情况下，查询是通过执行全表扫描进行的。第2种情况是，没有支持查询的哈希索引，但存在有序索引。使用有序索引意味着将执行并发范围扫描。由于顺序仅保存在本地分区上，需要在所有分区上执行索引扫描。</div>
	<div>
		MaxNoOfConcurrentScans的默认值是256。最大值为500。</div>
	<div>
		该参数指定了事务协调器中的可能扫描数。如果未提供本地扫描记录的数目，会对其进行计算，等于MaxNoOfConcurrentScans乘以系统中数据节点的数目。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;<b>[NDBD]MaxNoOfLocalScans</b></div>
	<div>
		如果很多扫描不是完全并行化的，指定本地扫描记录的数目。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;<b>[NDBD]BatchSizePerLocalScan</b></div>
	<div>
		该参数用于计算锁定记录的数目，要想处理很多并发扫描操作，需要这类记录。</div>
	<div>
		默认值是64，该值与SQL节点中定义的ScanBatchSize关系密切。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<b>&nbsp;[NDBD]LongMessageBuffer</b></div>
	<div>
		这是用于在单独节点内和节点之间传递消息的内部缓冲。尽管几乎不需要改变它，但它仍是可配置的。默认情况下，它被设置为1MB。</div>
	<div>
		日志和Checkpointing</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;<b>[NDBD]NoOfFragmentLogFiles</b></div>
	<div>
		该参数用于设置节点的REDO日志文件的大小。REDO日志文件是按循环方式组织的。第1个和最后1个日志文件（有时也分别称为&ldquo;头&rdquo;日志文件和&ldquo;尾&rdquo;日志文件）不应相遇，这点极其重要，当它们彼此过于接近时，由于缺少新日志记录的空间，节点将开始放弃所有事务，包括更新。</div>
	<div>
		自插入日志记录开始，在三个本地检查点完成之前，不会删除REDO日志记录。检查点的频率由其自己的配置参数集决定，请参见本章的相应部分。</div>
	<div>
		默认的参数值为8，它表示有8个集合，每个集合有4个16MB文件，总容量为512MB。换句话讲，REDO日志空间必须按64MB的块大小分配。在需要大量更新的情况下，可能需要将NoOfFragmentLogFiles的值增加到300或更高，以便为REDO日志提供足够的空间。</div>
	<div>
		如果checkpointing很慢，并有很多对数据库的写操作以至于日志文件已满，而且在没有jeapo rdising恢复功能的情况下无法截断日志尾部，那么所有的更新日志均将被放弃，并给出错误代码410或缺少临时日志空间。该状况将一直持续，直至完成了检查点操作并能将日志尾部向前移动为止。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<b>&nbsp;[NDBD]MaxNoOfSavedMessages</b></div>
	<div>
		该参数用于设置跟踪文件的最大数目，在覆盖旧文件之前，将保留这些跟踪文件。无论出于何种原因，当节点崩溃时将创建跟踪文件。</div>
	<div>
		默认为25个跟踪文件。</div>
	<div>
		元数据对象</div>
	<div>
		下一组参数为元数据对象定义了池的大小，可用于定义最大属性数，表，索引，索引使用的触发程序对象，事件，以及簇之间的复制。注意，这些参数仅是对簇的&ldquo;建议&rdquo;，任何未指定的参数均将采用其默认值。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp;&nbsp;<b>&nbsp; [NDBD]MaxNoOfAttributes</b></div>
	<div>
		定义了可在簇中定义的属性数目。</div>
	<div>
		该参数的默认值为1000，最小的可能值为32。没有最大值限制。对于每一属性，每节点约需200字节的存储空间，这是应为，所有的元数据将完整地复制到服务器上。</div>
	<div>
		设置MaxNoOfAttributes时，应实现准备好打算在将来执行的任何ALTER TABLE命令，这点很重要。这是因为下述事实，在簇表上执行ALTER TABLE的过程中，所使用的属性数目是原始表中的3倍。例如，如果某一表需要100个属性，而且你打算在以后更改它，那么就需要将MaxNoOfAttributes的值设为300。有一个良好的经验规则，如果你能在不出现问题的情况下创建所有所需的表，请将最大表中属性数目的两倍加到MaxNoOfAttributes上。完成该设置后，应通过执行实际的ALTER TABLE操作，验证该数目是足够的。如果失败，将原始值的倍数加到MaxNoOfAttributes上，并再次测试。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]MaxNoOfTables</strong></div>
	<div>
		表对象是为每个表、唯一哈希索引和有序索引分配的。该参数为作为整体的簇设置了最大表对象数目。</div>
	<div>
		对于具有BLOB数据类型的每个属性，将使用额外的表来保存大部分BLOB数据。定义表的总数时，必须将这些表考虑在内。</div>
	<div>
		该参数的默认值为128。最小值为8，最大值为1600。每个表对象每节点约需20KB的空间。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]MaxNoOfOrderedIndexes</strong></div>
	<div>
		对于簇中的每个有序索引，将分配1个对象，该对象描述了编入索引的是什么以及其存储段。默认情况下，每个这样定义的索引还将定义1个有序索引。每个唯一索引和主键既有1个有序索引还有1个哈希索引。</div>
	<div>
		该参数的默认值为128。每个对象每节点约需10KB的数据。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]MaxNoOfUniqueHashIndexes</strong></div>
	<div>
		对于每个不是主键的唯一索引，将分配1个特殊表，该表将唯一键映射到索引表的主键上。默认情况下，对于每个唯一索引，还将定义1个有序索引。为了防止该情况，定义唯一索引时，必须使用USING HASH选项。</div>
	<div>
		默认值是64。每个索引每节点约需15KB的空间。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]MaxNoOfTriggers</strong></div>
	<div>
		对于每个唯一性哈希索引，将分配内部更新、插入、和删除触发程序（这意味着对于每个唯一性哈希索引，将创建三个触发程序）。但是，1个有序索引仅需要1个触发程序对象。对于簇中每个正常表，备份也将使用三个触发程序对象。</div>
	<div>
		注释：支持簇之间的复制时，也将使用内部触发程序。</div>
	<div>
		该参数用于设置簇中触发程序对象的最大数目。</div>
	<div>
		该参数的默认值为768.</div>
	<div>
		&nbsp;</div>
	<div>
		<strong>布尔参数</strong></div>
	<div>
		&nbsp;</div>
	<div>
		数据节点的行为也会受具有布尔值的一组参数的影响。将其设为&ldquo;1&rdquo;或&ldquo;Y&rdquo;，可将这类参数设置为&ldquo;真&rdquo;，将其设为&ldquo;0&rdquo;或&ldquo;N&rdquo;，可将这类参数设置为&ldquo;假&rdquo;。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]LockPagesInMainMemory</strong></div>
	<div>
		对于包括Solaris和Linux在内的很多操作系统，能够将进程锁定在内存中，以避免与磁盘的交换。使用它，可确保簇的实时特性。</div>
	<div>
		默认情况下，该特性是被禁止的。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]StopOnError</strong></div>
	<div>
		出现错误时，该参数指定了NDBD进程是退出还是执行自动重启。</div>
	<div>
		默认情况下，允许该特性。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]Diskless</strong></div>
	<div>
		能够将MySQL簇的表指定为&ldquo;无磁盘的&rdquo;，这意味着不会在磁盘上对表执行检查点操作，也不会出现日志操作。这类表仅存在于主内存中。使用&ldquo;无磁盘&rdquo;表的一个结果是，出现崩溃侯，不会保留这类表，也不会保留这类表中的任何记录。但是，当工作在&ldquo;无磁盘&rdquo;模式下时，能够在无盘计算机上运行ndbd。</div>
	<div>
		要点：该特性会使整个簇运行在&ldquo;无磁盘&rdquo;模式下。</div>
	<div>
		允许该特性时，可执行备份操作，但不会实际保存备份数据。</div>
	<div>
		将&ldquo;Diskless&rdquo;设置为&ldquo;1&rdquo;或&ldquo;Y&rdquo;可允许该特性。默认情况下，禁止该特性。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]RestartOnErrorInsert</strong></div>
	<div>
		仅当创建调试版时才能访问该特性，在执行作为测试组成部份的代码块的过程中，可以插入错误。</div>
	<div>
		默认情况下，该特性是被禁止的。</div>
	<div>
		控制超时、间隔、和磁盘分页</div>
	<div>
		有多种用于指定超时以及簇数据节点中各种动作间时间间隔的参数。大多数超时值以毫秒为单位指定。任何例外均将在适用时指明。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]TimeBetweenWatchDogCheck</strong></div>
	<div>
		为了防止主线程在某一点上陷入无限循环，采用了&ldquo;看门狗&rdquo;线程来检查主线程。该参数以毫秒为单位指定了检查之间的时间间隔。如果三次检查之后进程仍保持在相同的状态，它将被&ldquo;看门狗&rdquo;线程中止。</div>
	<div>
		出于试验目的，可方便地更改该参数，也可以对其进行调整以适合本地条件。也可以按节点指定它，虽然这样作的理由很少。</div>
	<div>
		默认超时为4000毫秒（4秒）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; <strong>&nbsp; [NDBD]StartPartialTimeout</strong></div>
	<div>
		该参数指定了在调用簇初始化子程序之前，簇等待所有存储节点出现的时间。该超时参数由于防止部分簇启动。</div>
	<div>
		默认值是30000毫秒（30秒）。0表示无限超时，换句话讲，仅当所有节点均可能时才会启动簇。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]StartPartitionedTimeout</strong></div>
	<div>
		等待了StartPartialTimeout毫秒后，如果簇做好了启动准备但仍可能处于隔离状态，簇将等待该超时时间结束。</div>
	<div>
		默认超时为60000毫秒（60秒）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; <strong>&nbsp; [NDBD]StartFailureTimeout</strong></div>
	<div>
		如果数据节点在该参数指定的时间内未完成其启动序列，节点启动将失败。如果将该参数设置为0，表示不采用数据节点超时。</div>
	<div>
		默认值是60000毫秒(60秒）。对于包含大量数据的数据节点，应增加该参数。例如，对于包含数GB数据的存储节点，为了执行节点重启，可能需要10～15分钟（即600000～1000000毫秒）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]HeartbeatIntervalDbDb</strong></div>
	<div>
		发现失败节点的主要方法之一是使用&ldquo;心跳&rdquo;数。该参数指明了心跳信号的发送频率，以及接收它们的频率。如果在1行内丢失了三次心跳，节点将被宣告为死亡。因此，通过心跳机制发现故障的最大时间是心跳间隔的四倍。</div>
	<div>
		默认的心跳间隔为1500毫秒（1.5秒）。不得大幅度更改该参数，各节点间该参数的变化范围也不得过宽。例如，如果某一节点使用了5000毫米的值，而观察它的节点采用1000毫秒，很显然，该节点很快就会被宣布为死亡。能够在软件升级期间更改该参数，但增量应较小。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; <strong>&nbsp; [NDBD]HeartbeatIntervalDbApi</strong></div>
	<div>
		每个数据节点会将心跳信号发送到各MySQL服务器（SQL节点），以确保保持接触。如果某一MySQL服务器未能及时发出心跳信号，它将被宣布为死亡。在这种情况下，所有正在进行的事务将结束并释放所有资源。SQL节点不能重新连接，直至由以前的MySQL实例初始化的所有活动完成为止。用于该判断的3心跳判据与HeartbeatIntervalDbDb描述的相同。</div>
	<div>
		默认时间间隔为1500毫秒（1.5秒）。不同的数据节点之间，该间隔可以有所不同，这是因为，每个存储节点均会独立于所有其他数据节点观察与之相连的MySQL服务器。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp;<strong> &nbsp; [NDBD]TimeBetweenLocalCheckpoints</strong></div>
	<div>
		该参数是一个例外，它未指定启动新的本地检查前应等待的时间，相反，它用于确保在出现相对较少更新的簇内未执行本地检查点操作。在具有较高更新率的大多数簇内，很可能在前一个本地检查点操作完成后立刻启动一个新的检查点操作。</div>
	<div>
		从前一个本地检查点启动后，所有已执行写操作的大小将增加。该参数也是一个例外，原因在于它被指定为4字节字总数的以2为底数的对数，因此，默认值20表示4MB (4 &times; 220)写操作，21表示8MB，依此类推，直至等同于8GB写操作的最大值31。</div>
	<div>
		簇中所有的写操作将加在一起。将TimeBetweenLocalCheckpoints设置为6或更小表示本地检查点操作将不停顿地连续执行，与簇的工作负荷无关。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]TimeBetweenGlobalCheckpoints</strong></div>
	<div>
		提交事务时，它被提交到存有镜像数据的所有节点的主内存中。但是，事务日志记录不会作为提交进程的一部分写入磁盘。其原因在于，在至少两台独立主机机器上安全体提交事务应能满足关于关于持久性的合理标准。</div>
	<div>
		另一个很重要的方面是，应确保即使在最差情况下（簇完全崩溃），也能进行恰当地处理。为了确保这点，在给定时间间隔内出现的所有事务均会被放到全局检查点，可将其视为写入磁盘的已提交事务的集合。换句话讲，作为提交进程的组成部分，事务将被放入全局检查点组；稍后，该组的日志记录将被写入磁盘，然后将整个事务组安全地提交到簇内所有计算机的磁盘上。。</div>
	<div>
		该参数定义了全局检查点操作之间的时间间隔。默认值为2000毫秒。 milliseconds.</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]TimeBetweenInactiveTransactionAbortCheck</strong></div>
	<div>
		对于该参数指定的每个时间间隔，通过检查每个事务的定时器来执行超时处理。因此，如果该参数被设为1000毫秒，每隔1秒就会对事务进行检查。</div>
	<div>
		该参数的默认值为1000毫秒（1秒）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]TransactionInactiveTimeout</strong></div>
	<div>
		如果事务目前未执行任何查询，而是等待进一步的用户输入，该参数指明了放弃事务之前用户能够等待的最长时间。</div>
	<div>
		该参数的默认值是0（无超时）。对于需要确保无任何事务锁定了过长时间的数据库，应将参数设置为较小的值。单位为毫秒。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]TransactionDeadlockDetectionTimeout</strong></div>
	<div>
		当节点执行涉及事务的查询时，在继续之前，节点将等待簇中其他节点作出回应。如果出现下述原因，将无法予以回应：</div>
	<div>
		1. &nbsp; &nbsp;节点&ldquo;死亡&rdquo;。</div>
	<div>
		2. &nbsp; &nbsp;操作进入锁定队列。</div>
	<div>
		3. &nbsp; &nbsp;被请求执行动作的节点负荷过重。</div>
	<div>
		该超时参数指明了放弃事务之前，事务协调器等候另一节点执行查询的时间长短，该参数在节点失败处理和死锁检测方面十分重要。在涉及死锁和节点失败的情形下，如果将其设置的过高，会导致不合需要的行为。</div>
	<div>
		默认的超时值为1200毫秒（1.2秒）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]NoOfDiskPagesToDiskAfterRestartTUP</strong></div>
	<div>
		执行本地检查点操作时，相应的算法会将所有数据页写入磁盘。如果追求尽快完成该操作而不是适中，很可能会对处理器、网络和磁盘带来过重负担。为了控制写入速度，该参数指明了每100毫秒可写入多少数据页。在本情形下，1个数据页定义为8KB，因而该参数的单位是每秒80KB。因此，如果将NoOfDiskPagesToDiskAfterRestartTUP设置为20，那么在执行本地检查点操作期间，要求每秒想磁盘写入1.6MB的数据。该值包括针对数据页的UNDO日志记录写入，也就是说，该参数能处理来自数据内存的写入限制。置于针对索引页的UNDO日志记录，它们是由参数NoOfDiskPagesToDiskAfterRestartACC处理的（关于索引页的更多信息，请参见关于IndexMemory的条目）。</div>
	<div>
		简而言之，该参数指定了执行本地检查点操作的速度，并能与NoOfFragmentLogFiles、DataMemory和IndexMemory一起使用。</div>
	<div>
		默认值是40（每秒3.2MB的数据页）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]NoOfDiskPagesToDiskAfterRestartACC</strong></div>
	<div>
		该参数使用的单位与NoOfDiskPagesToDiskAfterRestartTUP的相同，工作方式也类似，但限制的是从索引内存进行的索引页写入速度。</div>
	<div>
		该参数的默认值为每秒20个索引内存页（1.6MB每秒）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]NoOfDiskPagesToDiskDuringRestartTUP</strong></div>
	<div>
		该参数的工作方式类似于NoOfDiskPagesToDiskAfterRestartTUP和NoOfDiskPagesToDiskAfterRestartACC，但仅对重启节点时在节点内执行的本地检查点操作有效。作为所有节点重启的组成部份，总会执行本地检查点操作。在节点重启过程中，能够以比其他时间更快的速度执行磁盘写入操作，这是因为，此时在节点内执行的活动数较少。</div>
	<div>
		该参数涉及从数据内存写入的页。</div>
	<div>
		默认值是40（3.2MB每秒）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; <strong>&nbsp; [NDBD]NoOfDiskPagesToDiskDuringRestartACC</strong></div>
	<div>
		在节点重启的本地检查点阶段，对能够写入到磁盘的索引内存页的数目进行控制。</div>
	<div>
		与NoOfDiskPagesToDiskAfterRestartTUP和NoOfDiskPagesToDiskAfterRestartACC一样，该参数的值采用的单位也是每100毫秒写入8KB（80KB/秒）。</div>
	<div>
		默认值是20 (1.6MB每秒）。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]ArbitrationTimeout</strong></div>
	<div>
		该参数指定了数据节点等待仲裁程序对仲裁消息的回应的时间。如果超过了该时间，将假定网络已断开。</div>
	<div>
		默认值是1000毫秒（1秒）。</div>
	<div>
		&nbsp;</div>
	<div>
		<strong>缓冲和日志功能</strong></div>
	<div>
		&nbsp;</div>
	<div>
		一些与以前的编译时间参数对应的配置参数仍可用。使用这些参数，高级用户能够对节点进程使用的资源进行更多的控制，并能根据需要调整各种缓冲区大小。</div>
	<div>
		将日志记录写入磁盘时，这些缓冲区用作文件系统的前端。如果节点运行在无盘模式下，那么可以将这些参数设置为它们的最小值而不会造成负面影响，这是因为，磁盘写入是由NDB存储引擎的文件系统提取层虚拟的。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp;<strong> &nbsp; [NDBD]UndoIndexBuffer</strong></div>
	<div>
		该缓冲用于本地检查点操作执行期间。NDB存储引擎采用了一种恢复方案，该方案建立在检查点一致性以及操作性REDO日志值上。为了在不隔断整个系统的写操作的情况下获得一致的检查点，在执行本地检查点操作的同时，将执行UNDO日志操作。UNDO日志功能每次是在单个表偏短上触发的。由于表全部保存在主内存中，该优化是可能的。</div>
	<div>
		UNDO索引缓冲用于主键哈希索引上的更新。插入和删除操作会导致哈希索引的重新排列，NDB存储引擎将映射了所有物理变化的UNDO日志记录写入索引页，以便能在系统重启时撤销这些变化。它还能记录启动本地检查点操作时对每个偏短的所有插入操作。</div>
	<div>
		读取和更新能够设置锁定位，并更新哈希索引条目中的标题。这类变更由页写入算法负责处理，以确保这些操作不需要UNDO日志。</div>
	<div>
		该缓冲的默认大小为2MB。最小值为1MB，对于大多数应用，最小值已足够。对于执行极大和／或大量插入和删除操作、并处理大事务和大主键的应用程序，或许有必要增大该缓冲。如果该缓冲过小，NDB存储引擎会发出错误代码677&ldquo;索引UNDO缓冲过载&rdquo;。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp; <strong>[NDBD]UndoDataBuffer</strong></div>
	<div>
		UNDO数据缓冲的作用与UNDO索引缓冲的相同，不同之处在于，它作用在数据内存上而不是索引内存上。对于插入、删除和更新，该缓冲是在片段的本地检查点阶段使用的。</div>
	<div>
		由于UNDO日志条目会随着所记录操作的增加而增大，该缓冲大于与之对应的索引内存缓冲，默认值为16MB。</div>
	<div>
		对于某些应用程序，该内存可能过大。在这种情况下，可降低它的值，最小为1MB。</div>
	<div>
		需要增加该缓冲的情况十分罕见。如果确实有这方面的要求，较好的方式是，检查磁盘是否能实际处理数据库更新活动所产生的负荷。如果缺少足够的磁盘空间，即使增加该缓冲的大小也不能解决问题。</div>
	<div>
		如果该缓冲过小并变得&ldquo;拥挤不堪&rdquo;，NDB存储引擎将发出错误代码891&ldquo;数据UNDO缓冲过载&rdquo;。</div>
	<div>
		&middot; &nbsp; &nbsp; &nbsp; &nbsp;<strong> [NDBD]RedoBuffer</strong></div>
	<div>
		所有的更新活动也需要被记录到日志中。使用这类日志，当系统重启时，能够重现这类更新。NDB恢复算法采用了&ldquo;模糊&rdquo;数据检查点和UNDO日志，然后使用REDO日志再现所有变化直至到达恢复点。</div>
	<div>
		该缓冲的默认大小是8MB。最小值为1MB。</div>
	<div>
		如果该缓冲过小，NDB存储引擎将发出错误代码1221&ldquo;REDO日志缓冲过载&rdquo;。</div>
	<div>
		在管理簇的过程中，应能控制为各种事件类型发送至标准输出装置的日志消息的数目，这点十分重要。有16种可能的事件级别（编号从0到15）。如果将给定事件类别的事件通报级别设置为15，那么该类别中的所有事件报告均会被发送至标准输出装置，如果将其设置为0，表示在该类别中的没有事件报告。</div>
	<div>
		默认情况下，仅会将启动消息发送至标准输出装置，其余的事件通报级别默认为0。这样做的原因在于，这些消息也会被发送至管理服务器的簇日志。</div>
	<div>
		对于管理客户端，也能设置类似的级别，用以确定在簇日志中记录哪些级别的事件。</div>
</div>

